import tensorflow as tf
import logging
import numpy as np


class NoteDecisionModel:
    BATCH_SIZE = 1
    NOTE_MAX = 16
    HIDDEN_LSTM = 32
    NUMBER_OF_CELLS = 5
    INPUT_SIZE = 1
    OUTPUT_SIZE = 1
    EPS = 1e-6
    LEARNING_RATE = 0.01

    def __init__(self):
        self.series_left = []
        self.series_right = []
        self.session = None

        self.inputs = tf.placeholder(tf.float32, (None, None, self.INPUT_SIZE))
        self.outputs = tf.placeholder(tf.float32, (None, None, self.OUTPUT_SIZE))
        lstm_cells = []
        for _ in range(self.NUMBER_OF_CELLS):
            lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(self.HIDDEN_LSTM, state_is_tuple=True)
            lstm_cells.append(lstm_cell)
        multi_rnn_cell = tf.nn.rnn_cell.MultiRNNCell(lstm_cells)
        initial_state = multi_rnn_cell.zero_state(tf.shape(self.inputs)[1], tf.float32)
        rnn_outputs, rnn_states = tf.nn.dynamic_rnn(multi_rnn_cell, self.inputs, initial_state=initial_state, time_major=True)

        def final_projection(x):
            return tf.contrib.layers.linear(x, num_outputs=self.OUTPUT_SIZE, activation_fn=tf.nn.sigmoid)

        self.predicted_outputs = tf.map_fn(final_projection, rnn_outputs)
        self.error = -(self.outputs * tf.log(self.predicted_outputs + self.EPS) + (1.0 - self.outputs)
                       * tf.log(1.0 - self.predicted_outputs + self.EPS))
        error = tf.reduce_mean(self.error)
        self.train_function = tf.train.AdamOptimizer(learning_rate=self.LEARNING_RATE).minimize(error)

    def predict_note(self, last_note):
        test_x = []
        for current_note in range(self.NOTE_MAX):
            test_x.append([last_note, current_note])

        batch_size = 1
        logging.info('epoch start')
        x = np.empty((1, batch_size, 1))
        for i in range(batch_size):
            x[:, i, 0] = last_note

        prediction = self.session.run(self.predicted_outputs, {
            self.inputs: x
        })
        logging.info('prediction')
        logging.info(prediction)
        logging.info(round(prediction[0][0][0]))
        return int(round(prediction[0][0][0]))

    def train(self, series_left, series_right):
        logging.info('init train')

        init = tf.global_variables_initializer()
        self.session = tf.Session()
        # For some reason it is our job to do this:
        self.session.run(init)

        logging.info('start train')
        for i in range(len(series_left)):
            left = series_left[i]
            right = series_right[i]

            logging.info('epoch start')
            x = np.empty((1, self.BATCH_SIZE, 1))
            y = np.empty((1, self.BATCH_SIZE, 1))

            for b in range(self.BATCH_SIZE):
                x[:, b, 0] = left
                y[:, b, 0] = right

            logging.info('epoch train start')
            epoch_error = self.session.run([self.error, self.train_function], {
                self.inputs: x,
                self.outputs: y,
            })
            logging.info('epoch')
            logging.info(epoch_error)
        logging.info('trained')
