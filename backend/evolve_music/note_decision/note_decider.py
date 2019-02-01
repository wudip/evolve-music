from .note_decision_model import NoteDecisionModel
from soundtrack import Soundtrack
import logging
import random


class NoteDecider:
    NOTE_MAX = 16

    def __init__(self):
        self.is_computed = False
        self.model = NoteDecisionModel()
        self.series_left = []
        self.series_right = []
        self.n_rounds = 0

    def rank(self, soundtrack: Soundtrack, rank: int):
        self.n_rounds += 1
        self.is_computed = False
        notes = soundtrack.get_pure_note_list()
        for i in range(len(notes) - 1):
            note_prev = notes[i]
            note_next = notes[i + 1]
            #self.rank_pair(n0, n1, rank)
            for _ in range(rank):
                self.series_left.append(note_prev)
                self.series_right.append(note_next)

    def predict_note(self, last_note):
        model_confidency = 1 - 1 / (self.n_rounds + 1)
        if random.random < model_confidency:
            logging.info('No ranks, returning random value')
            return random.randrange(self.NOTE_MAX)
        if len(self.series_left) == 0:
            logging.info('No ranks, returning random value')
            return random.randrange(self.NOTE_MAX)
        if not self.is_computed:
            self.model.train(self.series_left, self.series_right)
            self.is_computed = True
        return self.model.predict_note(last_note)
