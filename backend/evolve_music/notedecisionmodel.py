import tensorflow as tf
from soundtrack import Soundtrack
import sys
import logging


class NoteDecisionModel:
    NOTE_MAX = 8

    def __init__(self):
        self.rank_pairs = []
        self.ranks = []
        self.input_data = tf.placeholder(tf.float32, (None, 2))
        self.input_labels = tf.placeholder(tf.float32, (None, 1))
        self.model = self.create_model()

        learning_rate = 0.05
        batch_loss = tf.nn.softmax_cross_entropy_with_logits(labels=self.input_labels, logits=self.model)
        self.loss = tf.reduce_mean(batch_loss)
        self.goal = tf.train.GradientDescentOptimizer(learning_rate).minimize(self.loss)
        self.session = None
        self.is_computed = False

    def create_model(self):
        layer1 = tf.layers.dense(self.input_data, 2, activation=tf.nn.relu)
        layer2 = tf.layers.dense(layer1, 50, activation=tf.nn.relu)
        logits = tf.layers.dense(layer2, 1)

        return logits

    def get_weights(self, last_note):
        if len(self.ranks) == 0:
            logging.info('No ranks')
            print('No ranks', file=sys.stderr)
            return [100 / self.NOTE_MAX] * self.NOTE_MAX
        if not self.is_computed:
            self.compute()
        test_x = []
        for current_note in range(self.NOTE_MAX):
            test_x.append([last_note, current_note])
        prediction = self.session.run(self.model, feed_dict={
            self.input_data: test_x
        })

        weights = []
        weight_sum = 0
        for i in range(self.NOTE_MAX):
            weight = prediction[i][0]
            if weight < 0:
                weight = 0
            weight_sum += weight
            weights.append(weight)
        logging.info('weights')
        logging.info(weights)
        for i in range(self.NOTE_MAX):
            weights[i] *= 100 / weight_sum
        return weights

    def rank(self, soundtrack: Soundtrack, rank: int):
        self.is_computed = False
        notes = soundtrack.get_pure_note_list()
        for i in range(len(notes) - 1):
            n0 = notes[i]
            n1 = notes[i + 1]
            self.rank_pair(n0, n1, rank)

    def rank_pair(self, note0, note1, rank):
        self.rank_pairs.append([note0, note1])
        self.ranks.append([rank])

    def compute(self):
        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        batch_loss = self.session.run([self.loss, self.goal], feed_dict={
            self.input_data: self.rank_pairs,
            self.input_labels: self.ranks
        })
        logging.info('Batch')
        print('Batch', file=sys.stderr)
        print(batch_loss, file=sys.stderr)
        self.is_computed = True

