import argparse
import numpy as np
import os
import psutil
import time
import logging
import tensorflow.compat.v1 as tf1

from fastavro import parse_schema
from gdmix.io.dataset_metadata import DatasetMetadata
from gdmix.io.input_data_pipeline import per_record_input_fn
from gdmix.models.api import Model
from gdmix.models.custom.base_lr_argparser import parser as lr_parser
from gdmix.models.photon_ml_writer import PhotonMLWriter
from gdmix.util import constants
from gdmix.util.distribution_utils import shard_input_files
from gdmix.util.io_utils import read_json_file, try_write_avro_blocks, str2bool, export_scipy_lr_model_to_avro,\
    load_scipy_models_from_avro, copy_files
from scipy.optimize import fmin_l_bfgs_b
from tensorflow.python.ops import collective_ops


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

tf1.disable_eager_execution()


def logging(msg):
    """ logging util. """
    logger.info("[LBFGS] {}".format(msg))


class FixedEffectLRModelLBFGS(Model):
    """
    Logstic regression model with scipy LBFGS + TF.
    """
    # TF all reduce op group identifier
    TF_ALL_REDUCE_GROUP_KEY = 0

    def __init__(self, raw_model_params, base_training_params):
        self.model_params = self._parse_parameters(raw_model_params)
        self.training_output_dir = base_training_params[constants.TRAINING_OUTPUT_DIR]
        self.validation_output_dir = base_training_params[constants.VALIDATION_OUTPUT_DIR]
        self.local_training_input_dir = "local_training_input_dir"
        self.model_params[constants.FEATURE_BAGS] = list(self.model_params[constants.FEATURE_BAGS].split(','))
        self.lbfgs_iteration = 0
        self.training_data_path = self.model_params[constants.TRAIN_DATA_PATH]
        self.validation_data_path = self.model_params[constants.VALIDATION_DATA_PATH]
        self.metadata_file = self.model_params[constants.METADATA_FILE]
        self.feature_file = self.model_params[constants.FEATURE_FILE]
        self.checkpoint_path = self.model_params[constants.MODEL_OUTPUT_DIR]
        self.data_format = self.model_params[constants.DATA_FORMAT]

        self.feature_bag_name = self.model_params[constants.FEATURE_BAGS][0]
        self.offset_column_name = self.model_params[constants.OFFSET]

        self.batch_size = int(self.model_params[constants.BATCH_SIZE])
        self.copy_to_local = self.model_params[constants.COPY_TO_LOCAL]
        self.num_correction_pairs = self.model_params[constants.NUM_OF_LBFGS_CURVATURE_PAIRS]
        self.factor = self.model_params[constants.LBFGS_TOLERANCE] / np.finfo(float).eps
        self.is_regularize_bias = self.model_params[constants.REGULARIZE_BIAS]
        self.max_iteration = self.model_params[constants.NUM_OF_LBFGS_ITERATIONS]
        self.l2_reg_weight = self.model_params[constants.L2_REG_WEIGHT]

        self.metadata = self._load_metadata()
        self.tensor_metadata = DatasetMetadata(self.metadata_file)
        self.global_num_samples = self.tensor_metadata.get_number_of_training_samples()
        self.num_features = self._get_num_features()
        self.model_coefficients = None

        self.server = None

        # validate parameters:
        assert len(self.model_params[constants.FEATURE_BAGS]) == 1, "Only support one feature bag"
        assert self.global_num_samples > 0,\
            "Number of training samples must be set in the metadata and be positive"
        assert self.feature_file and tf1.io.gfile.exists(self.feature_file), \
            "feature file {} doesn't exist".format(self.feature_file)

    def _load_metadata(self):
        """ Read metadata file from json format. """
        assert tf1.io.gfile.exists(self.metadata_file), "metadata file %s does not exist" % self.metadata_file
        return read_json_file(self.metadata_file)

    @staticmethod
    def _get_assigned_files(input_data_path, num_shards, shard_index):
        """
        Get the assigned files from the shard
        :param input_data_path:
        :return: a list of assigned file names.
        """
        assigned_files, sample_level_shard = shard_input_files(input_data_path, num_shards, shard_index)
        assert not sample_level_shard, "Doesn't support sample level sharding," \
                                       "number of files must >= number of workers"
        return assigned_files

    def _get_num_features(self):
        """ Get number of features from metadata. """
        num_features = next(filter(lambda x: x.name == self.feature_bag_name,
                                   self.tensor_metadata.get_features())).shape[0]
        assert num_features > 0, "number of features must > 0"
        return num_features

    def _has_feature(self, feature_column_name):
        """ Check if tensor schema has the provided feature field. """
        return feature_column_name in self.tensor_metadata.get_feature_names()

    def _has_label(self, label_column_name):
        """ Check if tensor schema has the provided label field. """
        return label_column_name in self.tensor_metadata.get_label_names()

    def _create_server(self, execution_context):
        if self.server:
            return
        cluster_spec = execution_context[constants.CLUSTER_SPEC]
        task_index = execution_context[constants.TASK_INDEX]
        config = tf1.ConfigProto()
        config.experimental.collective_group_leader = '/job:worker/replica:0/task:0'
        self.server = tf1.distribute.Server(cluster_spec,
                                            config=config,
                                            job_name='worker',
                                            task_index=task_index)

    def _inference_model_fn(self, diter, x_placeholder, num_iterations, schema_params):
        """ Implement the forward pass to get logit. """
        sample_id_list = tf1.constant([], tf1.int64)
        label_list = tf1.constant([], tf1.int64)
        weight_list = tf1.constant([], tf1.float32)
        prediction_score_list = tf1.constant([], tf1.float64)
        prediction_score_per_coordinate_list = tf1.constant([], tf1.float64)

        feature_bag_name = self.feature_bag_name
        sample_id_column_name = schema_params[constants.SAMPLE_ID]
        label_column_name = schema_params[constants.LABEL]
        sample_weight_column_name = schema_params[constants.SAMPLE_WEIGHT]
        offset_column_name = self.offset_column_name
        has_offset = self._has_feature(offset_column_name)
        has_label = self._has_label(label_column_name)
        has_weight = self._has_feature(sample_weight_column_name)
        i = tf1.constant(0, tf1.int64)

        def cond(i, sample_id_list, label_list, weight_list, prediction_score_list, prediction_score_per_coordinate_list):
            return tf1.less(i, num_iterations)

        def body(i, sample_id_list, label_list, weight_list, prediction_score_list, prediction_score_per_coordinate_list):
            i += 1
            all_features, all_labels = diter.get_next()
            features = all_features[feature_bag_name]
            sample_ids = all_features[sample_id_column_name]
            current_batch_size = tf1.shape(sample_ids)[0]
            offsets = all_features[offset_column_name] if has_offset else tf1.zeros(current_batch_size, tf1.float64)
            weights = all_features[sample_weight_column_name] if has_weight \
                else tf1.ones(current_batch_size, tf1.float32)
            labels = all_labels[label_column_name] if has_label else tf1.zeros(current_batch_size, tf1.int64)

            sample_id_list = tf1.concat([sample_id_list, sample_ids], axis=0)
            weight_list = tf1.concat([weight_list, weights], axis=0)
            label_list = tf1.concat([label_list, labels], axis=0)

            w = x_placeholder[:-1]
            b = x_placeholder[-1]
            logits = tf1.sparse.sparse_dense_matmul(tf1.cast(features, tf1.float64),
                                                    tf1.cast(tf1.expand_dims(w, 1), tf1.float64))\
                + tf1.expand_dims(tf1.ones(current_batch_size, tf1.float64) * tf1.cast(b, tf1.float64), 1)
            prediction_score_per_coordinate_list = tf1.concat([prediction_score_per_coordinate_list,
                                                               tf1.reshape(logits, [-1])], axis=0)

            logits_with_offsets = logits + tf1.expand_dims(tf1.cast(offsets, tf1.float64), 1)
            prediction_score_list = tf1.concat([prediction_score_list, tf1.reshape(logits_with_offsets, [-1])], axis=0)

            return i, sample_id_list, label_list, weight_list, prediction_score_per_coordinate_list, prediction_score_list

        _, sample_id_list, label_list, weight_list, prediction_score_per_coordinate_list, prediction_score_list \
            = tf1.while_loop(cond, body,
                             loop_vars=[i, sample_id_list, label_list, weight_list,
                                        prediction_score_per_coordinate_list, prediction_score_list],
                             shape_invariants=[i.get_shape()] + [tf1.TensorShape([None])] * 5)

        return sample_id_list, label_list, weight_list, prediction_score_per_coordinate_list, prediction_score_list

    def _train_model_fn(self, diter, x_placeholder, num_workers, num_features, global_num_samples, num_iterations,
                        schema_params):
        """ The training objective function and the gradients. """
        value = tf1.constant(0.0, tf1.float64)
        # Add bias
        gradients = tf1.constant(np.zeros(num_features + 1))
        feature_bag_name = self.feature_bag_name
        label_column_name = schema_params[constants.LABEL]
        sample_weight_column_name = schema_params[constants.SAMPLE_WEIGHT]
        offset_column_name = self.offset_column_name
        is_regularize_bias = self.is_regularize_bias
        has_weight = self._has_feature(sample_weight_column_name)
        has_offset = self._has_feature(offset_column_name)
        i = 0

        def cond(i, value, gradients):
            return i < num_iterations

        def body(i, value, gradients):
            i += 1
            all_features, all_labels = diter.get_next()
            features = all_features[feature_bag_name]
            labels = all_labels[label_column_name]
            current_batch_size = tf1.shape(labels)[0]
            weights = all_features[sample_weight_column_name] if has_weight else tf1.ones(current_batch_size,
                                                                                          tf1.float64)
            offsets = all_features[offset_column_name] if has_offset else tf1.zeros(current_batch_size, tf1.float64)

            w = x_placeholder[:-1]
            b = x_placeholder[-1]
            logits = tf1.sparse.sparse_dense_matmul(tf1.cast(features, tf1.float64),
                                                    tf1.cast(tf1.expand_dims(w, 1), tf1.float64)) \
                + tf1.expand_dims(tf1.ones(current_batch_size, tf1.float64) * tf1.cast(b, tf1.float64), 1) \
                + tf1.expand_dims(tf1.cast(offsets, tf1.float64), 1)

            loss = tf1.nn.sigmoid_cross_entropy_with_logits(labels=tf1.cast(labels, tf1.float64),
                                                            logits=tf1.reshape(tf1.cast(logits, tf1.float64), [-1]))
            weighted_loss = tf1.cast(weights, tf1.float64) * loss
            # regularzer has the option to include or exclude bias
            regularizer = tf1.nn.l2_loss(x_placeholder) if is_regularize_bias else tf1.nn.l2_loss(w)
            batch_value = tf1.reduce_sum(weighted_loss) + regularizer * self.l2_reg_weight \
                * tf1.cast(current_batch_size, tf1.float64) / global_num_samples
            batch_gradients = tf1.gradients(batch_value, x_placeholder)[0]
            value += batch_value
            gradients += batch_gradients
            return i, value, gradients

        _, value, gradients = tf1.while_loop(cond, body, [i, value, gradients])

        if num_workers > 1:
            # sum all reduce
            reduced_value = collective_ops.all_reduce(
                value, num_workers, FixedEffectLRModelLBFGS.TF_ALL_REDUCE_GROUP_KEY, 0,
                merge_op='Add', final_op='Id')
            reduced_gradients = collective_ops.all_reduce(
                gradients, num_workers, FixedEffectLRModelLBFGS.TF_ALL_REDUCE_GROUP_KEY, 1,
                merge_op='Add', final_op='Id')
            return reduced_value, reduced_gradients
        else:
            return value, gradients

    def _compute_loss_and_gradients(self, x, tf_session, x_placeholder, ops, task_index):
        """ Compute loss and gradients, invoked by Scipy LBFGS solver. """
        self.lbfgs_iteration += 1

        start_time = time.time()
        init_dataset_op, value_op, gradients_op = ops
        tf_session.run(init_dataset_op)
        value, gradients = tf_session.run([value_op, gradients_op], feed_dict={x_placeholder: x})
        logging("Iteration {}: value = {}".format(self.lbfgs_iteration, value))
        logging("Iteration {}: memory used: {} GB".format(self.lbfgs_iteration, self._check_memory()))
        logging("Iteration {}: --- {} seconds ---".format(self.lbfgs_iteration, time.time() - start_time))
        return value, gradients

    def _write_inference_result(self, sample_ids, labels, weights, scores,
                                scores_and_offsets, task_index, schema_params, output_dir):
        """ Write inference results. """
        photon_ml_writer = PhotonMLWriter(schema_params=schema_params)
        output_avro_schema = photon_ml_writer.get_inference_output_avro_schema(
            self.metadata,
            self._has_label(schema_params[constants.LABEL]),
            True,
            has_weight=self._has_feature(schema_params[constants.SAMPLE_WEIGHT]))
        parsed_schema = parse_schema(output_avro_schema)

        records = []
        for rec_id, rec_label, rec_weight, rec_score, rec_score_and_offset in \
                zip(sample_ids, labels, weights, scores, scores_and_offsets):
            rec = {schema_params[constants.SAMPLE_ID]: int(rec_id),
                   schema_params[constants.PREDICTION_SCORE]: float(rec_score),
                   schema_params[constants.PREDICTION_SCORE_PER_COORDINATE]: float(rec_score_and_offset)
                   }
            if self._has_label(schema_params[constants.LABEL]):
                rec[schema_params[constants.LABEL]] = int(rec_label)
            if self._has_feature(schema_params[constants.SAMPLE_WEIGHT]):
                rec[schema_params[constants.SAMPLE_WEIGHT]] = int(rec_weight)
            records.append(rec)

        output_file = os.path.join(output_dir, "part-{0:05d}.avro".format(task_index))
        error_msg = "worker {} encountered error in writing inference results".format(task_index)
        with tf1.gfile.GFile(output_file, 'wb') as f:
            try_write_avro_blocks(f, parsed_schema, records, None, error_msg)
        logging("Worker {} saved inference result to {}".format(task_index, output_file))

    # TODO(mizhou): All inference results are saved to memory and then write once, give the observation
    # of samll inference result size (each sample size is only 24 bytes), may need revisiting.
    def _run_inference(self, x, tf_session, x_placeholder, ops, task_index, schema_params, output_dir):
        """ Run inference on training or validation dataset. """
        start_time = time.time()
        sample_ids_op, labels_op, weights_op, scores_op, scores_and_offsets_op = ops
        sample_ids, labels, weights, scores, scores_and_offsets = tf_session.run(
            [sample_ids_op, labels_op, weights_op, scores_op, scores_and_offsets_op],
            feed_dict={x_placeholder: x})

        self._write_inference_result(sample_ids, labels, weights, scores, scores_and_offsets, task_index,
                                     schema_params, output_dir)
        logging("Inference --- {} seconds ---".format(time.time()-start_time))

    def _check_memory(self):
        """ Check memory usage. """
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1e9

    def _get_num_iterations(self, input_files):
        """ Get the number of samples each worker assigned.
            This works for tfrecord only.
        """
        local_num_samples = 0
        for fname in input_files:
            local_num_samples += sum(1 for _ in tf1.python_io.tf_record_iterator(fname))
        num_iterations = int(local_num_samples / self.batch_size) + (1 if local_num_samples % self.batch_size else 0)
        return num_iterations

    def train(self, training_data_path, validation_data_path, metadata_file, checkpoint_path,
              execution_context, schema_params):
        """ Overwrite train method from parent class. """
        logging("Kicking off fixed effect LR LBFGS training")

        task_index = execution_context[constants.TASK_INDEX]
        num_workers = execution_context[constants.NUM_WORKERS]
        is_chief = execution_context[constants.IS_CHIEF]
        self._create_server(execution_context)

        assigned_train_files = self._get_assigned_files(training_data_path, num_workers, task_index)
        if self.copy_to_local:
            train_input_dir = self.local_training_input_dir
            actual_train_files = copy_files(assigned_train_files, train_input_dir)
            # After copy the worker's shard to local, we don't shard the local files any more.
            train_num_shards = 1
            train_shard_index = 0
        else:
            train_input_dir = self.training_data_path
            actual_train_files = assigned_train_files
            train_num_shards = num_workers
            train_shard_index = task_index

        # Define the graph here, keep session open to let scipy L-BFGS solver repeatly call _compute_loss_and_gradients
        with tf1.variable_scope('worker{}'.format(task_index)), \
                tf1.device('job:worker/task:{}/device:CPU:0'.format(task_index)):

            # Define ops for training
            train_dataset = per_record_input_fn(train_input_dir,
                                                metadata_file,
                                                train_num_shards,
                                                train_shard_index,
                                                self.batch_size,
                                                self.data_format)
            train_diter = tf1.data.make_initializable_iterator(train_dataset)
            init_train_dataset_op = train_diter.initializer
            train_x_placeholder = tf1.placeholder(tf1.float64, shape=[None])
            train_num_iterations = self._get_num_iterations(actual_train_files)
            value_op, gradients_op = self._train_model_fn(train_diter,
                                                          train_x_placeholder,
                                                          num_workers,
                                                          self.num_features,
                                                          self.global_num_samples,
                                                          train_num_iterations,
                                                          schema_params)
            train_ops = (init_train_dataset_op, value_op, gradients_op)

            # Define ops for inference
            valid_dataset = per_record_input_fn(validation_data_path,
                                                metadata_file,
                                                num_workers,
                                                task_index,
                                                self.batch_size,
                                                self.data_format)
            inference_x_placeholder = tf1.placeholder(tf1.float64, shape=[None])

            inference_train_data_diter = tf1.data.make_one_shot_iterator(train_dataset)
            train_sample_ids_op, train_labels_op, train_weights_op, train_scores_op, train_scores_and_offsets_op = self._inference_model_fn(
                inference_train_data_diter,
                inference_x_placeholder,
                train_num_iterations,
                schema_params)

            inference_validation_data_diter = tf1.data.make_one_shot_iterator(valid_dataset)
            assigned_validation_files = self._get_assigned_files(validation_data_path, num_workers, task_index)
            validation_data_num_iterations = self._get_num_iterations(assigned_validation_files)
            valid_sample_ids_op, valid_labels_op, valid_weights_op, valid_scores_op, valid_scores_and_offsets_op = self._inference_model_fn(
                inference_validation_data_diter,
                inference_x_placeholder,
                validation_data_num_iterations,
                schema_params)

            if num_workers > 1:
                all_reduce_sync_op = collective_ops.all_reduce(
                    tf1.constant(0.0, tf1.float64),
                    num_workers,
                    FixedEffectLRModelLBFGS.TF_ALL_REDUCE_GROUP_KEY,
                    0,
                    merge_op='Add',
                    final_op='Id')

            init_variables_op = tf1.global_variables_initializer()

        session_creator = tf1.train.ChiefSessionCreator(master=self.server.target)
        tf_session = tf1.train.MonitoredSession(session_creator=session_creator)
        tf_session.run(init_variables_op)

        # Run all reduce warm up
        logging("All-reduce-warmup starts...")
        if num_workers > 1:
            start_time = time.time()
            tf_session.run([all_reduce_sync_op])
            logging("All-reduce-warmup --- {} seconds ---".format(time.time() - start_time))

        # Start training
        logging("Training starts...")
        start_time = time.time()
        self.model_coefficients, f_min, info = fmin_l_bfgs_b(
            func=self._compute_loss_and_gradients,
            x0=np.zeros(self.num_features + 1),
            approx_grad=False,
            m=self.num_correction_pairs,  # number of variable metrics corrections. default is 10.
            factr=self.factor,            # control precision, smaller the better.
            maxiter=self.max_iteration,
            args=(tf_session, train_x_placeholder, train_ops, task_index),
            disp=0)
        logging("Training --- {} seconds ---".format(time.time() - start_time))
        logging("\n------------------------------\nf_min: {}\nnum of funcalls: {}\ntask msg:"
                "{}\n------------------------------".format(f_min, info['funcalls'], info['task']))

        logging("Inference training data starts...")
        inference_training_data_ops = (train_sample_ids_op, train_labels_op, train_weights_op, train_scores_op, train_scores_and_offsets_op)
        self._run_inference(self.model_coefficients,
                            tf_session,
                            inference_x_placeholder,
                            inference_training_data_ops,
                            task_index,
                            schema_params,
                            self.training_output_dir)

        logging("Inference validation data starts...")
        inference_validation_data_ops = (valid_sample_ids_op, valid_labels_op, valid_weights_op, valid_scores_op, valid_scores_and_offsets_op)
        self._run_inference(self.model_coefficients,
                            tf_session,
                            inference_x_placeholder,
                            inference_validation_data_ops,
                            task_index,
                            schema_params,
                            self.validation_output_dir)

        # Final sync up and then reliably terminate all workers
        if (num_workers > 1):
            tf_session.run([all_reduce_sync_op])

        tf_session.close()

        if is_chief:
            self._save_model()

        # remove the cached training input files
        if self.copy_to_local:
            tf1.gfile.DeleteRecursively(self.local_training_input_dir)

    def _save_model(self):
        """ Save the trained linear model in avro format. """
        weights = self.model_coefficients[:-1]
        bias = self.model_coefficients[-1]
        list_of_weight_indices = np.arange(weights.shape[0])
        output_file = os.path.join(self.checkpoint_path, "global_model.avro")
        export_scipy_lr_model_to_avro(model_ids=["global model"],
                                      list_of_weight_indices=np.expand_dims(list_of_weight_indices, axis=0),
                                      list_of_weight_values=np.expand_dims(weights, axis=0),
                                      biases=np.expand_dims(bias, axis=0),
                                      feature_file=self.feature_file,
                                      output_file=output_file)

    def _load_model(self):
        """ Load model from avro file. """
        logging("Loading model from {}".format(self.checkpoint_path))
        assert self.checkpoint_path and tf1.io.gfile.exists(self.checkpoint_path), "checkpoint path {} doesn't exist".format(self.checkpoint_path)
        model_file = tf1.io.gfile.glob("{}/*.avro".format(self.checkpoint_path))
        assert len(model_file) == 1, "Load model failed, no model file or multiple model files found in the model diretory {}".format(self.checkpoint)
        models = load_scipy_models_from_avro(model_file[0])
        return models[0]

    def export(self, output_model_dir):
        logging("No need model export for LR model. ")

    def predict(self,
                output_dir,
                input_data_path,
                metadata_file,
                checkpoint_path,
                execution_context,
                schema_params):
        # Overwrite predict method from parent class.
        logging("Kicking off fixed effect LR predict")

        task_index = execution_context[constants.TASK_INDEX]
        num_workers = execution_context[constants.NUM_WORKERS]
        # Prediction uses local server
        self.server = tf1.train.Server.create_local_server()

        # Define the graph here, keep session open to let scipy L-BFGS solver repeatly call _compute_loss_and_gradients
        # Inference is conducted in local mode.
        with tf1.variable_scope('worker{}'.format(task_index)), tf1.device('device:CPU:0'):
            dataset = per_record_input_fn(input_data_path,
                                          metadata_file,
                                          num_workers,
                                          task_index,
                                          self.batch_size,
                                          self.data_format)
            x_placeholder = tf1.placeholder(tf1.float64, shape=[None])

            data_diter = tf1.data.make_one_shot_iterator(dataset)
            assigned_files = self._get_assigned_files(input_data_path, num_workers, task_index)
            data_num_iterations = self._get_num_iterations(assigned_files)
            sample_ids_op, labels_op, weights_op, scores_op, scores_and_offsets_op = self._inference_model_fn(
                data_diter,
                x_placeholder,
                data_num_iterations,
                schema_params)
            init_variables_op = tf1.global_variables_initializer()

        session_creator = tf1.train.ChiefSessionCreator(master=self.server.target)
        tf_session = tf1.train.MonitoredSession(session_creator=session_creator)
        tf_session.run(init_variables_op)

        predict_ops = (sample_ids_op, labels_op, weights_op, scores_op, scores_and_offsets_op)
        model_coefficients = self._load_model()
        self._run_inference(model_coefficients,
                            tf_session,
                            x_placeholder,
                            predict_ops,
                            task_index,
                            schema_params,
                            output_dir)
        tf_session.close()

    def _parse_parameters(self, raw_model_parameters):
        parser = argparse.ArgumentParser(parents=[lr_parser])

        # Training parameters
        parser.add_argument("--" + constants.COPY_TO_LOCAL, type=str2bool, nargs='?', const=True, required=False, default=True,
                            help="Boolean for copying data to local or not.")
        model_params, other_args = parser.parse_known_args(raw_model_parameters)
        model_params_dict = vars(model_params)
        """validate the parameters"""
        assert int(model_params_dict[constants.BATCH_SIZE]) > 0, "Batch size must be positive number"
        return model_params_dict
