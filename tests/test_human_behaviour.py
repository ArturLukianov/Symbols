#!/usr/bin/env python3

import os, sys
sys.path.append('.')
sys.path.append('..')

from src.core import *


def test_human_eat_food():
    h = Human()
    f = Cucumber()
    f.value = 1000
    h.hunger = 300
    h.inventory.append(f)

    for i in range(10):
        h.update(None, 500)

    assert len(h.inventory) == 0
    assert h.hunger > 300


def test_human_get_food():
    tile = Tile()
    h = Human()
    f = Cucumber()

    f.value = 1000
    h.hunger = 300

    tile.items.append(f)
    tile.chars.append(h)

    max_turns = 100

    for i in range(max_turns):
        tile.update(i)
        print(h.hunger)

    assert h.hunger > 1000


def test_human_sleep():
    h = Human()

    h.update(None, 0)
    assert h.status == 'sleeping'

def test_human_starve():
    h = Human()
    t = Tile()

    for i in range(1000):
        h.update(t, i)

    assert h.hunger <= 0
    assert not h.is_alive
