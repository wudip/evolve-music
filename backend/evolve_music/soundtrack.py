import base64


class Soundtrack:
    def __init__(self):
        self.rank = 0

    def set_rank(self, rank):
        self.rank = rank

    def to_midi(self):
        with open("sample.mid", "rb") as binary_file:
            data = binary_file.read()
            return base64.b64encode(data).decode('ascii')
