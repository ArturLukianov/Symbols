#!/usr/bin/env python3

import os, sys
sys.path.append('.')
sys.path.append('..')

from src.core import *


def test_peasant_planting():
    p = HumanPeasant()
    s = CucumberSeeds()
    s.value = 10
    s.water_multiplier = 0
    loc = Location()
    field = Field()

    p.inventory.append(s)

    loc.chars.append(p)
    loc.connect(field)

    for i in range(100):
        loc.update(600 + i)
        field.update(600 + i)

    assert field.seeds_count == 10


def test_peasant_gathering():
    p = HumanPeasant()
    loc = Location()
    field = Field()
    c = Cucumber()

    field.fruits.append(c)
    loc.chars.append(p)
    loc.connect(field)

    for i in range(200):
        loc.update(600 + i)
        field.update(600 + i)

    assert len(p.inventory) != 0
    assert len(field.fruits) == 0


def test_peasant_work_cycle():
    p = HumanPeasant()
    p.hunger = 100000
    loc = Location()
    field = Field()
    s = CucumberSeeds()
    s.value = 10
    s.water_multiplier = 0

    p.inventory.append(s)
    loc.chars.append(p)
    loc.connect(field)

    for i in range(800):
        loc.update(500 + i)
        field.update(500 + i)

    assert len(p.inventory) != 0
    assert p.inventory[0].is_food


def test_peasant_can_keep_alive():
    p = HumanPeasant()
    loc = Location()
    field = Field()
    c = Cucumber()
    well = Well()

    p.inventory.append(c)
    loc.chars.append(p)
    loc.connect(field)
    loc.connect(well)

    for i in range(31 * 1000):
        loc.update(i)

    assert p.is_alive


def test_peasant_water_plants():
    p = HumanPeasant()
    loc = Location()
    field = Field()
    s = CucumberSeeds()
    well = Well()

    loc.chars.append(p)
    loc.connect(field)
    loc.connect(well)
    field.plant(s)

    for i in range(80):
        loc.update(600 + i)
        field.update(600 + i)
        well.update(600 + i)

    assert len(field.seeds) > 0
    assert field.seeds[0].water > 0
