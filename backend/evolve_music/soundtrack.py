import base64
from EasyMIDI import EasyMIDI, Track, Note
import io
import random


class Soundtrack:
    def __init__(self):
        self.rank = 0
        self.genome = []
        for i in range(6):
            rand = random.randint(0, 6)
            rand_octave = random.randint(4, 6)
            self.genome.append((rand, rand_octave))

    def set_rank(self, rank):
        self.rank = rank

    def to_midi(self):
        easy_midi = EasyMIDI()
        track1 = Track("acoustic grand piano")
        note_arr = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        notes = []
        for note_encoded in self.genome:
            note_id, note_octave = note_encoded
            note_name = note_arr[note_id]
            note = Note(note_name, octave=note_octave, duration=1 / 8, volume=100)
            notes.append(note)
        track1.addNotes(notes)
        easy_midi.addTrack(track1)
        out_str = io.BytesIO()
        easy_midi.midFile.writeFile(out_str)
        data = out_str.getvalue()
        out_str.close()
        return base64.b64encode(data).decode('ascii')
