from .item import Resource, Water

class Location(object):
    name = None
    items = []
    chars = []
    locs = []


    def update(self, time):
        for char in self.chars:
            char.update(self, time)

        for item in self.items:
            item.update(self, time)


    def __getattr__(self, name):
        if name.startswith('is_'):
            return False
        return object.__getattribute__(self, name)

    def connect(self, loc):
        self.locs.append(loc)
        loc.locs.append(self)




class Field(Location):
    name = 'Field'
    is_plantable = True

    seeds_count = 0
    seeds = []
    fruits = []

    def plant(self, seeds):
        self.seeds_count += seeds.value
        seeds.is_planted = True
        seeds.is_pickable = False
        self.seeds.append(seeds)

    def update(self, time):
        ind_to_pop = []
        for ind, seed in enumerate(self.seeds):
            seed.turns_to_grow -= 1
            seed.water -= seed.value * seed.water_multiplier
            if seed.water <= 0:
                ind_to_pop.append(ind)
                continue
            if seed.turns_to_grow <= 0:
                for i in range(seed.value):
                    self.fruits.append(seed.plant())
                ind_to_pop.append(ind)
                self.seeds_count -= seed.value

        for ind in ind_to_pop:
            self.seeds.pop(ind)


class WaterSource(Location):
    is_water_source = True
    value = 10

    def get_water(self):
        water = Water()
        water.value = self.value
        return water


class Well(WaterSource):
    name = "Well"
    value = 100


class ResourceSource(Location):
    resource = 'stone'
    def __init__(self, amount):
        self.amount = amount

    def take_resource(self):
        if self.amount > 0:
            self.amount -= 1
        return Resource(self.resource)


class Mine(ResourceSource):
    is_mine = True

class Forest(ResourceSource):
    is_forest = True