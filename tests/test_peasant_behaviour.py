#!/usr/bin/env python3

import os, sys
sys.path.append('.')
sys.path.append('..')

from src.core import *


def test_peasant_planting():
    p = HumanPeasant()
    s = CucumberSeeds()
    s.value = 10
    tile = Tile()
    field = Field()

    p.inventory.append(s)

    tile.chars.append(p)
    tile.items.append(field)

    for i in range(200):
        tile.update(600)

    assert field.seeds_count == 10


def test_peasant_gathering():
    p = HumanPeasant()
    tile = Tile()
    field = Field()
    c = Cucumber()

    field.fruits.append(c)
    tile.items.append(field)
    tile.chars.append(p)

    for i in range(200):
        tile.update(600)

    assert len(p.inventory) != 0
    assert len(field.fruits) == 0
