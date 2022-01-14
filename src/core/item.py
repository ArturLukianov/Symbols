class Item(object):
    name = None

    def update(self, tile, time):
        pass

    def __getattr__(self, name):
        if name.startswith('is_'):
            return False
        return object.__getattribute__(self, name)



class Food(Item):
    is_food = True
    value = 0


class Fruit(Food):
    is_fruit = True
    seeds = None

    @classmethod
    def set_seeds(cls, seeds_cls):
        cls.seeds = seeds_cls
        return seeds_cls

class Cucumber(Fruit):
    name = 'cucumber'
    value = 1000


class Seeds(Item):
    is_seed = True
    is_planted = False
    value = 0

@Cucumber.set_seeds
class CucumberSeeds(Seeds):
    name = 'cucumber seeds'
    plant = Cucumber
    turns_to_grow = 100
    value = 3
    water = 200
    water_multiplier = 1


class Water(Item):
    is_water = True
    value = 1

