class Item(object):
    name = None

    def update(self, tile, time):
        pass

    def __getattr__(self, name):
        if name.startswith('is_'):
            return False



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
    seeds_count = 3


class Seeds(Item):
    is_seed = True
    is_planted = False
    value = 0

@Cucumber.set_seeds
class CucumberSeeds(Seeds):
    name = 'cucumber seeds'
    plant = Cucumber
    turns_to_grow = 100


class Field(Item):
    is_pickable = False
    is_ground = True

    seeds_count = 0
    seeds = []
    fruits = []

    def plant(self, seeds):
        self.seeds_count += seeds.value
        seeds.is_planted = True
        seeds.is_pickable = False
        self.seeds.append(seeds)

    def update(self, tile, time):
        ind_to_pop = []
        for ind, seed in enumerate(self.seeds):
            seed.turns_to_grow -= 1
            if seed.turns_to_grow <= 0:
                for i in range(seed.value):
                    self.fruits.append(seed.plant())
                ind_to_pop.append(ind)

        for ind in ind_to_pop:
            self.seeds.pop(ind)
