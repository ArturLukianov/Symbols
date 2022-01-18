#!/usr/bin/env python3

import sys

sys.path.append('.')
sys.path.append('..')

from src.core import *


def test_human_eat_food():
    '''Test that human can eat food from her inventory'''
    human = Human()
    food = Cucumber()
    food.value = 1000
    human.hunger = 300
    human.inventory.append(food)

    for _ in range(10):
        human.update(500)

    assert human.hunger > 300


def test_human_get_food():
    '''Test that human can get food from current location'''
    loc = Location(None, (0, 0))
    human = Human()
    food = Cucumber()

    food.value = 1000
    human.hunger = 300

    loc.items.append(food)
    loc.add_char(human)

    max_turns = 100

    for i in range(max_turns):
        loc.update(i)

    assert human.hunger > 1000


def test_human_sleep():
    '''Test that human is sleeping when night'''
    human = Human()

    for _ in range(20):
        human.update(0)
    assert human.status == 'sleeping'


def test_human_starve():
    '''Test that human is starving to death without food'''
    human = Human()
    loc = Location(None, (0, 0))

    loc.add_char(human)

    for i in range(1000):
        loc.update(i)

    assert human.hunger <= 0
    assert not human.is_alive
