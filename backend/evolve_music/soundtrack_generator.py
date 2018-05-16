from soundtrack import Soundtrack
from notedecisionmodel import NoteDecisionModel
import random
import math


class SoundtrackGenerator:
    SOUNDTRACK_LEN_DEFAULT = 4
    POSSIBLE_DURATIONS = [1/4, 1/8]
    NOTE_MAX = 8

    def __init__(self):
        self.model = NoteDecisionModel()
        pass

    def generate_soundtrack(self, round = 1):
        s = Soundtrack()
        last_note = random.randrange(self.NOTE_MAX)
        length = int(self.SOUNDTRACK_LEN_DEFAULT + math.floor(round / 2))
        for i in range(length):
            weights = self.model.get_weights(last_note)
            note_id = self.note_from_weights(weights)
            duration_index = random.randrange(len(self.POSSIBLE_DURATIONS))
            duration = self.POSSIBLE_DURATIONS[duration_index]
            s.add_note(note_id, duration)
            last_note = note_id
        return s

    @staticmethod
    def note_from_weights(weights):
        weight_sum = 0.0
        r = random.randrange(100)
        selected = 0
        while weight_sum < r and selected < len(weights):
            weight_sum += weights[selected]
            selected += 1
        return selected

    def rank(self, soundtrack, rank):
        self.model.rank(soundtrack, rank)
