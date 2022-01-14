from .item import Resource, Water, Ore, Wood

class Location(object):
    name = 'Location'
    color = 'gray'
    size = 5

    def __init__(self):
        self.items = []
        self.chars = []
        self.locs = []


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

    def add_char(self, char):
        self.chars.append(char)
        char.loc = self

    def to_d3(self):
        return {
            'id': id(self),
            'label': self.name,
            'color': self.color,
            'size': self.size * 10
        }




class Field(Location):
    name = 'Field'
    color = 'green'
    is_plantable = True
    size = 20

    seeds_count = 0

    def __init__(self):
        super().__init__()
        self.seeds = []
        self.fruits = []

    def plant(self, seeds):
        self.seeds_count += seeds.value
        seeds.is_planted = True
        seeds.is_pickable = False
        self.seeds.append(seeds)

    def update(self, time):
        super().update(time)

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

        if len(ind_to_pop) != 0:
            new_seeds = []
            for ind, seed in enumerate(self.seeds):
                if ind not in ind_to_pop:
                    new_seeds.append(seed)
            self.seeds = new_seeds


class WaterSource(Location):
    is_water_source = True
    value = 10
    color = 'blue'
    size = 10

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
        super().__init__()
        self.amount = amount
        self.size = int(amount * 1.2)

    def take_resource(self):
        if self.amount > 0:
            self.amount -= 1
        return Resource(self.resource)


class Mine(ResourceSource):
    name = 'Mine'
    is_mine = True
    resource = 'iron'
    color = 'brown'

    def take_resource(self):
        if self.amount > 0:
            self.amount -= 1
        return Ore(self.resource)

class Forest(ResourceSource):
    is_forest = True
    resource = 'pine'

    def take_resource(self):
        if self.amount > 0:
            self.amount -= 1
        return Wood(self.resource)
