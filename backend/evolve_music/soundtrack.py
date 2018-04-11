import base64
from EasyMIDI import EasyMIDI,Track,Note,Chord,RomanChord
import random
import io

class Soundtrack:
    def __init__(self):
        self.rank = 0

    def set_rank(self, rank):
        self.rank = rank

    def to_midi(self):
        easyMIDI = EasyMIDI()
        track1 = Track("acoustic grand piano")
        note_arr = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        notes = []
        for i in range(6):
            rand = random.randint(0, 6)
            rand_octave = random.randint(4, 6)
            note_name = note_arr[rand]
            note = Note(note_name, octave=rand_octave, duration=1 / 4, volume=100)
            notes.append(note)
        track1.addNotes(notes)
        easyMIDI.addTrack(track1)
        out_str = io.BytesIO()
        easyMIDI.midFile.writeFile(out_str)
        data = out_str.getvalue()
        out_str.close()
        return base64.b64encode(data).decode('ascii')
