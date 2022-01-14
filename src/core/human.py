#!/usr/bin/env python3
import logging
import random

from .character import Character
from .utils import is_night, is_day, random_name


logger = logging.getLogger('symbols')
logger.setLevel(logging.INFO)


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
        self.short_memory_reset_timer = 100
        self.long_memory = dict()
        self.is_alive = True
        self.loc = None

        if self.profession is None:
            logger.info(f'New human "{self.name}" is created')
        else:
            logger.info(f'New human ({self.profession}) "{self.name}" is created')


    def log_status(self):
        if self.profession is None:
            logger.info(f'"{self.name}" [{self.hunger}] is {self.status} - {self.sub_status}')
        else:
            logger.info(f'"{self.name}" [{self.hunger}] ({self.profession}) is {self.status} - {self.sub_status}')

    def log_death(self, reason):
        logger.info(f'"{self.name}" died from {reason}')



    def change_sub_status(self, new_sub_status):
        if self.sub_status != new_sub_status:
            self.sub_status = new_sub_status
            self.log_status()

    def change_status(self, new_status):
        if self.status != new_status:
            self.status = new_status
            self.sub_status = None
            self.log_status()


    def go_to(self, next_loc):
        if self.loc is not None:
            self.loc.chars.remove(self)
        next_loc.add_char(self)

    def update(self, tile, time):
        if not self.is_alive:
            return

        self.short_memory_reset_timer -= 1
        if self.short_memory_reset_timer <= 0:
            self.short_memory.clear()
            self.short_memory_reset_timer = 100

        if self.hunger <= 0:
            self.log_death('hunger')
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
               self.status != 'getting food' and \
                   self.short_memory.get('has food', True):
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
               self.status != 'getting food' and \
                   self.short_memory.get('has food', True):
            self.change_status('eating')

        if self.status == 'resting':
            self.rest(tile, time)
            return

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

    def rest(self, tile, time):
        pass

    def eat(self, tile, time):
        if self.hunger > 700:
            self.change_status(None)
            return

        for ind, item in enumerate(self.inventory):
            if item.is_food:
                self.inventory.pop(ind)
                if item.is_fruit:
                    seeds = item.seeds()
                    self.inventory.append(seeds)
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

        for ind, character in enumerate(tile.chars):
            status = character.ask_food(self)
            if status:
                return

        self.short_memory['has food'] = False
        self.change_status(None)

    def go_sleep(self, tile, time):
        self.change_status('sleeping')


    def ask_food(self, asker):
        for i in range(len(self.inventory)):
            if self.inventory[i].is_food:
                food = self.inventory.pop(i)
                asker.inventory.append(food)
                return True
        return False
