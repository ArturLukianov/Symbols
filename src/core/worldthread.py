#!/usr/bin/env python3

from threading import Thread
import time


DELAY = 0.1


class WorldThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 locs=None):
        super(WorldThread, self).__init__(group=group,
                                          target=target,
                                          name=name)

        if locs is None:
            locs = []
        self.locs = locs
        self.timer = 0

    def run(self):
        while True:
            for loc in self.locs:
                loc.update(self.timer)
            time.sleep(DELAY)
            self.timer += 1
            pass
