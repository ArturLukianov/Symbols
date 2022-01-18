#!/usr/bin/env python3

from . import *
import random
import math


def generate_locations():
    locs = []
    for i in range(random.randint(20, 100)):
        dice = random.randint(0, 100)

        if dice < 10:
            locs.append(Mine(random.randint(10, 200)))
        elif dice < 15:
            locs.append(Well())
        elif dice < 90:
            locs.append(Location())
        else:
            locs.append(Field())

    for i in range(len(locs)):
        links = int(math.log(random.randint(4, 16), 4))
        for j in range(links):
            while True:
                connect_with = locs[random.randint(0, len(locs) - 1)]
                if connect_with not in locs[i].locs and \
                   connect_with != locs[i]:
                    locs[i].connect(connect_with)
                    break

        if random.randint(0, 100) > 80:
            locs[i].add_char(HumanPeasant())
            locs[i].chars[-1].inventory.append(Cucumber())

    return locs
