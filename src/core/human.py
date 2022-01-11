#!/usr/bin/env python3
import logging
import random

from .character import Character
from .utils import is_night, random_name


logger = logging.getLogger('symbols')
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)


class Human(Character):
    profession = None

    def __init__(self, name=None):
        if name is None:
            name = random_name()
        super().__init__(name)
        self.inventory = []
        self.habitation = None
        self.hunger = 1000
        self.is_awake = True
        self.status = None
        self.sub_status = None

        if self.profession is None:
            logger.info(f'New human "{self.name}" is created')
        else:
            logger.info(f'New human ({self.profession}) "{self.name}" is created')


    def update(self, tile, time):
        if not self.is_awake:
            self.status = 'sleeping'
            self.hunger -= 1
            return

        self.hunger -= 2

        if self.hunger < 600:
            self.status = 'eating'

        if is_night(time) and random.randint(0, 100) < 5 and self.status != 'eating':
            self.status = 'going to sleep'

        if self.status is None:
            self.status = 'working'

        if self.status == 'working':
            self.work(tile, time)
        if self.status == 'eating':
            self.eat(tile, time)
        if self.status == 'getting food':
            self.get_food(tile, time)
        if self.status == 'going to sleep':
            self.go_sleep(tile, time)

    def work(self, tile, time):
        pass

    def eat(self, tile, time):
        if self.hunger > 700:
            self.status = None
            return

        for ind, item in enumerate(self.inventory):
            if item.is_food:
                self.inventory.pop(ind)
                self.hunger += item.value
                return

        self.status = 'getting food'

    def get_food(self, tile, time):
        for item in self.inventory:
            if item.is_food:
                self.status = 'eating'
                return

        for ind, item in enumerate(tile.items):
            if item.is_food:
                tile.items.pop(ind)
                self.inventory.append(item)
                self.status = 'eating'
                return

    def go_sleep(self, tile, time):
        pass


class HumanPeasant(Human):
    profession = 'peasant'

    def work(self, tile, time):
        pass
