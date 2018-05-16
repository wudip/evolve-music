import base64
from EasyMIDI import EasyMIDI, Track, Note
import io
import sys
import math


class Soundtrack:
    GENOME_LEN = 5
    NOTE_ARR = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    OCTAVE_BASE = 3

    def __init__(self):
        self.notes = []
        self.pure_notes = []
        self.octaves = []
        self.durations = []
        self.volumes = []
        self.rank = 0

    def add_note(self, note_id: int, duration: float):
        note_octave = self.OCTAVE_BASE + math.floor(note_id / len(self.NOTE_ARR))
        note_tone_id = note_id % len(self.NOTE_ARR)
        note = self.NOTE_ARR[note_tone_id]
        self.pure_notes.append(note_id)
        self.notes.append(note)
        self.octaves.append(note_octave)
        volume = 100
        self.durations.append(duration)
        self.volumes.append(volume)

    def set_rank(self, rank):
        self.rank = rank

    def to_midi(self):
        easy_midi = EasyMIDI()
        track1 = Track("acoustic grand piano")
        notes = []
        for i in range(len(self.notes)):
            note_name = self.notes[i]
            note_octave = self.octaves[i]
            duration = self.durations[i]
            volume = self.volumes[i]
            note = Note(note_name, octave=note_octave, duration=duration, volume=volume)
            notes.append(note)
        track1.addNotes(notes)
        easy_midi.addTrack(track1)
        out_str = io.BytesIO()
        easy_midi.midFile.writeFile(out_str)
        data = out_str.getvalue()
        out_str.close()
        return base64.b64encode(data).decode('ascii')

    def get_pure_note_list(self):
        return self.pure_notes
