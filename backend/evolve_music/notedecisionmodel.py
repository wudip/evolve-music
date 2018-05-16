import tensorflow as tf
from soundtrack import Soundtrack
import logging
import numpy as np
import random


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
        self.rank_pairs = []
        self.ranks = []
        self.series_left = []
        self.series_right = []
        self.session = None
        self.is_computed = False

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
        if len(self.ranks) == 0:
            logging.info('No ranks, returning random value')
            return random.randrange(self.NOTE_MAX)
        if not self.is_computed:
            self.compute()
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

    def rank(self, soundtrack: Soundtrack, rank: int):
        self.is_computed = False
        notes = soundtrack.get_pure_note_list()
        for i in range(len(notes) - 1):
            n0 = notes[i]
            n1 = notes[i + 1]
            #self.rank_pair(n0, n1, rank)
            for _ in range(rank):
                self.series_left.append(n0)
                self.series_right.append(n1)

    def rank_pair(self, note0, note1, rank):
        self.rank_pairs.append([note0, note1])
        self.ranks.append([rank])

    def compute(self):
        logging.info('init train')

        init = tf.global_variables_initializer()
        self.session = tf.Session()
        # For some reason it is our job to do this:
        self.session.run(init)

        logging.info('start train')
        for i in range(len(self.series_left)):
            left = self.series_left[i]
            right = self.series_right[i]

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
        self.is_computed = True
