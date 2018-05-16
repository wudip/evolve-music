from soundtrack_generator import SoundtrackGenerator


class MusicGenerator:
    NUMBER_OF_SOUNDTRACKS = 3

    def __init__(self):
        self.sg = SoundtrackGenerator()
        self.soundtracks = None
        self.round = 0

    def rank_generation(self, ranks: list):
        if len(ranks) != len(self.soundtracks):
            return
        for soundtrack_id, rank in enumerate(ranks):
            soundtrack = self.soundtracks[soundtrack_id]
            self.sg.rank(soundtrack, rank)

    def get_music(self):
        self.soundtracks = []
        for i in range(self.NUMBER_OF_SOUNDTRACKS):
            self.soundtracks.append(self.sg.generate_soundtrack(self.round))
        self.round += 1
        return self.soundtracks
