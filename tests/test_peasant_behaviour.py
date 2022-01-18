#!/usr/bin/env python3

import os, sys
sys.path.append('.')
sys.path.append('..')

from src.core import *


def test_peasant_planting():
    '''Test peasant can plant seeds on nearby field'''
    world = World((1, 2))

    peasant = HumanPeasant()
    seeds = CucumberSeeds()
    seeds.value = 10
    seeds.water_multiplier = 0
    loc = Location(world, (0, 0))
    field = Field(world, (0, 0))

    world.set_loc((0, 0), loc)
    world.set_loc((0, 1), field)

    peasant.inventory.append(seeds)

    loc.add_char(peasant)

    for i in range(100):
        loc.update(600 + i)
        field.update(600 + i)

    assert field.seeds_count == 10


def test_peasant_gathering():
    world = World((1, 2))
    p = HumanPeasant()
    loc = Location(world, (0, 0))
    field = Field(world, (0, 1))
    c = Cucumber()
    p.hunger = 10000

    field.fruits.append(c)
    loc.add_char(p)

    for i in range(200):
        world.update(i + 1)

    assert len(p.inventory) != 0
    assert len(field.fruits) == 0


def test_peasant_work_cycle():
    world = World((1, 2))
    peasant = HumanPeasant()
    peasant.hunger = 100000
    loc = Location(world, (0, 0))
    field = Field(world, (0, 1))
    seeds = CucumberSeeds()
    seeds.value = 10
    seeds.water_multiplier = 0

    peasant.inventory.append(seeds)
    loc.add_char(peasant)

    for i in range(800):
        loc.update(500 + i)
        field.update(500 + i)

    assert len(peasant.inventory) != 0
    assert peasant.inventory[0].is_food


def test_peasant_can_keep_alive():
    world = World((2, 2))
    p = HumanPeasant()
    loc = Location(world, (0, 0))
    field = Field(world, (0, 1))
    c = CucumberSeeds()
    well = Well(world, (1, 1))

    p.inventory.append(c)
    loc.add_char(p)

    for i in range(31 * 1000):
        world.update(i)

    assert p.is_alive


def test_peasant_water_plants():
    world = World((2, 2))
    p = HumanPeasant()
    loc = Location(world, (0, 0))
    field = Field(world, (0, 1))
    s = CucumberSeeds()
    well = Well(world, (1, 1))

    loc.add_char(p)
    field.plant(s)

    for i in range(80):
        loc.update(600 + i)
        field.update(600 + i)
        well.update(600 + i)

    assert len(field.seeds) > 0
    assert field.seeds[0].water > 0
