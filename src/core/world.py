#!/usr/bin/env python3


from .location import Location


class World(object):

    def __init__(self, size):
        self.size = size
        self.locs = []
        for i in range(size[0]):
            self.locs.append([])
            for j in range(size[1]):
                self.locs[-1].append(None)

    def update(self, time):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.locs[i][j] is not None:
                    self.locs[i][j].update(time)


    def set_loc(self, pos, loc):
        self.locs[pos[0]][pos[1]] = loc
        loc.pos = pos
        loc.world = self
