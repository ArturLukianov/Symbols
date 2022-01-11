#!/usr/bin/env python3

import os, sys
sys.path.append('.')
sys.path.append('..')

from src.core import *


def test_human_eat_food():
    h = Human()
    f = Cucumber()
    f.value = 1000
    h.hunger = 500
    h.inventory.append(f)

    for i in range(10):
        h.update(None, 500)

    assert len(h.inventory) == 0 and h.hunger > 500


def test_human_get_food():
    tile = Tile()
    h = Human()
    f = Cucumber()

    f.value = 1000
    h.hunger = 500

    tile.items.append(f)
    tile.chars.append(h)

    max_turns = 200

    for i in range(max_turns):
        tile.update(i)

    assert h.hunger > 1000
