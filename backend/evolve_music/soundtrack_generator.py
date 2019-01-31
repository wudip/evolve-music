from soundtrack import Soundtrack
from note_decision.note_decider import NoteDecider
import random
import math


class SoundtrackGenerator:
    SOUNDTRACK_LEN_DEFAULT = 4
    POSSIBLE_DURATIONS = [1/4, 1/8]
    NOTE_MAX = 16

    def __init__(self):
        self.note_decision = NoteDecider()
        pass

    def generate_soundtrack(self, round_no=1):
        s = Soundtrack()
        last_note = random.randrange(self.NOTE_MAX)
        length = int(self.SOUNDTRACK_LEN_DEFAULT + math.floor(round_no / 2))
        for i in range(length):
            note_id = self.note_decision.predict_note(last_note)
            duration_index = random.randrange(len(self.POSSIBLE_DURATIONS))
            duration = self.POSSIBLE_DURATIONS[duration_index]
            s.add_note(note_id, duration)
            last_note = note_id
        return s

    def rank(self, soundtrack, rank):
        self.note_decision.rank(soundtrack, rank)
