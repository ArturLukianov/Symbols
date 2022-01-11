#!/usr/bin/env python3
import logging
import random

from .character import Character
from .utils import is_night, is_day, random_name


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
        self.name = name
        self.inventory = []
        self.habitation = None
        self.hunger = 1000
        self.status = None
        self.sub_status = None
        self.target = None
        self.short_memory = dict()
        self.short_memory_reset_timer = 200
        self.is_alive = True

        if self.profession is None:
            logger.info(f'New human "{self.name}" is created')
        else:
            logger.info(f'New human ({self.profession}) "{self.name}" is created')


    def log_status(self):
        if self.profession is None:
            logger.info(f'"{self.name}" [{self.hunger}] is {self.status} - {self.sub_status}')
        else:
            logger.info(f'"{self.name}" [{self.hunger}] ({self.profession}) is {self.status} - {self.sub_status}')


    def change_sub_status(self, new_sub_status):
        if self.sub_status != new_sub_status:
            self.sub_status = new_sub_status
            self.log_status()

    def change_status(self, new_status):
        if self.status != new_status:
            self.status = new_status
            self.sub_status = None
            self.log_status()


    def update(self, tile, time):
        if not self.is_alive:
            return

        self.short_memory_reset_timer -= 1
        if self.short_memory_reset_timer <= 0:
            self.short_memory = dict()
            self.short_memory_reset_timer = 200

        if self.hunger <= 0:
            self.is_alive = False

        if self.status == 'sleeping':
            self.hunger -= 1

            if self.hunger < 300 and \
               self.status != 'eating' and \
                   self.status != 'getting food':
                self.change_status('eating')
                return

            if is_day(time):
                self.change_status(None)
            else:
                return

        self.hunger -= 2

        if self.hunger < 300 and \
           self.status != 'eating' and \
               self.status != 'getting food':
            self.change_status('eating')
            return

        if is_night(time) and self.status != 'eating' and \
           self.status != 'getting food':
            self.change_status('sleeping')
            return

        if self.status is None:
            self.change_status('working')
            return

        if self.status == 'working':
            self.work(tile, time)
            return

        if self.hunger < 600 and \
           self.status != 'eating' and \
               self.status != 'getting food':
            self.change_status('eating')

        if self.status == 'eating':
            self.eat(tile, time)
            return

        if self.status == 'getting food':
            self.get_food(tile, time)
            return

        if self.status == 'going to sleep':
            self.go_sleep(tile, time)
            return

    def work(self, tile, time):
        pass

    def eat(self, tile, time):
        if self.hunger > 700:
            self.change_status(None)
            return

        for ind, item in enumerate(self.inventory):
            if item.is_food:
                self.inventory.pop(ind)
                if item.if_fruit:
                    self.inventory.append(item.seeds(item.seeds_count))
                self.hunger += item.value
                return

        self.change_status('getting food')

    def get_food(self, tile, time):
        for item in self.inventory:
            if item.is_food:
                self.change_status('eating')
                return

        for ind, item in enumerate(tile.items):
            if item.is_food:
                tile.items.pop(ind)
                self.inventory.append(item)
                self.change_status('eating')
                return

    def go_sleep(self, tile, time):
        self.change_status('sleeping')


class HumanPeasant(Human):
    profession = 'peasant'

    def work(self, tile, time):
        if self.sub_status == None:
            self.change_sub_status('checking fields')

        if self.sub_status == 'checking fields':
            if self.target is None or \
               not self.target.is_ground or \
               self.target in self.short_memory.get('checked fields', []):
                self.change_sub_status('going to unchecked ground')
            else:
                if len(self.target.fruits) != 0:
                    self.change_sub_status('gathering fruits')
                else:
                    has_seeds = False
                    for item in self.inventory:
                        if item.is_seed:
                           has_seeds = True
                           break
                    if has_seeds:
                        self.change_sub_status('planting')
                    else:
                        self.change_sub_status('checking fields')


        if self.sub_status == 'planting':
            planted = False
            for ind, item in enumerate(self.inventory):
                if item.is_seed:
                    self.target.plant(item)
                    self.inventory.pop(ind)
                    planted = True
                    break
            self.change_sub_status('checking fields')

        if self.sub_status == 'going to unchecked ground':
            for item in tile.items:
                if item.is_ground and \
                   item not in self.short_memory.get('checked grounds', []):
                    self.target = item
                    self.change_sub_status('checking fields')
                    break

        if self.sub_status == 'gathering fruits':
            self.inventory.append(self.target.fruits[0])
            self.target.fruits.pop(0)
            if len(self.target.fruits) == 0:
                self.change_sub_status('checking fields')
