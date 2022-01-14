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

    assert h.hunger > 300


def test_human_get_food():
    loc = Location()
    h = Human()
    f = Cucumber()

    f.value = 1000
    h.hunger = 300

    loc.items.append(f)
    loc.chars.append(h)

    max_turns = 100

    for i in range(max_turns):
        loc.update(i)
        print(h.hunger)

    assert h.hunger > 1000


def test_human_sleep():
    h = Human()

    for i in range(20):
        h.update(None, 0)
    assert h.status == 'sleeping'

def test_human_starve():
    h = Human()
    l = Location()

    for i in range(1000):
        h.update(l, i)

    assert h.hunger <= 0
    assert not h.is_alive
