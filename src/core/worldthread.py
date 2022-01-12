#!/usr/bin/env python3

from threading import Thread
import time


DELAY = 0.01


class WorldThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 tiles=None):
        super(WorldThread, self).__init__(group=group,
                                          target=target,
                                          name=name)

        if tiles is None:
            tiles = []
        self.tiles = tiles
        self.timer = 0

    def run(self):
        while True:
            for tile in self.tiles:
                tile.update(self.timer)
            time.sleep(DELAY)
            self.timer += 1
            pass
