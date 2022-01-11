class Tile(object):
    def __init__(self):
        self.items = []
        self.chars = []
        self.name = None
        self.enviroment = None

    def update(self, time):
        for char in self.chars:
            char.update(self, time)
