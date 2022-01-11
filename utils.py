#!/usr/bin/env python3
import random


DAY_LENGTH = 1000


def random_name():
    return ''.join([chr(ord('a') + random.randint(0, 25))
                    for i in range(random.randint(3, 5))]).capitalize()


def is_night(time):
    return (time % DAY_LENGTH) < DAY_LENGTH // 2

def is_day(time):
    return not is_night(time)
