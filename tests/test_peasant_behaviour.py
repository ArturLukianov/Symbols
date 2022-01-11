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

    for i in range(100):
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


def test_peasant_work_cycle():
    p = HumanPeasant()
    p.hunger = 100000
    tile = Tile()
    field = Field()
    s = CucumberSeeds()
    s.value = 10

    p.inventory.append(s)
    tile.items.append(field)
    tile.chars.append(p)

    for i in range(800):
        tile.update(600)

    assert len(p.inventory) != 0
    assert p.inventory[0].is_food


def test_peasant_can_keep_alive():
    p = HumanPeasant()
    tile = Tile()
    field = Field()
    c = Cucumber()

    p.inventory.append(c)
    tile.items.append(field)
    tile.chars.append(p)

    for i in range(31 * 1000):
        tile.update(i)

    assert p.is_alive
