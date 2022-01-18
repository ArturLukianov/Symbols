from .item import Resource, Water, Ore, Wood


mask = [
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0)
]


class Location(object):
    name = 'Location'
    color = 'gray'
    size = 5

    def __init__(self, world, pos):
        self.items = []
        self.chars = []
        self.pos = pos
        self.world = world
        if self.world is not None:
            world.set_loc(self.pos, self)


    def get_near_locs(self):
        locs = []
        for dx, dy in mask:
            nx = self.pos[0] + dx
            ny = self.pos[1] + dy
            if nx >= 0 and ny >= 0 and \
               nx < self.world.size[0] and ny < self.world.size[1] and \
               self.world.locs[nx][ny] is not None:
                locs.append(self.world.locs[nx][ny])
        return locs


    def update(self, time):
        for char in self.chars:
            char.update(time)

        for item in self.items:
            item.update(self, time)


    def __getattr__(self, name):
        if name.startswith('is_'):
            return False
        return object.__getattribute__(self, name)

    def add_char(self, char):
        self.chars.append(char)
        char.loc = self

    def to_d3(self):
        return {
            'id': id(self),
            'name': self.name,
            'color': self.color,
            'val': self.size
        }




class Field(Location):
    name = 'Field'
    color = 'saddlebrown'
    is_plantable = True
    size = 20

    seeds_count = 0

    def __init__(self, world, pos):
        super().__init__(world, pos)
        self.seeds = []
        self.fruits = []

    def plant(self, seeds):
        self.seeds_count += seeds.value
        seeds.is_planted = True
        seeds.is_pickable = False
        self.seeds.append(seeds)
        self.color = 'greenyellow'

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
                self.color = 'yellowgreen'
                ind_to_pop.append(ind)
                self.seeds_count -= seed.value

        if len(ind_to_pop) != 0:
            new_seeds = []
            for ind, seed in enumerate(self.seeds):
                if ind not in ind_to_pop:
                    new_seeds.append(seed)
            self.seeds = new_seeds

            if len(self.seeds) == 0 and len(self.fruits) == 0:
                self.color = 'saddlebrown'


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
    color = 'goldenrod'

    def take_resource(self):
        if self.amount > 0:
            self.amount -= 1
        return Ore(self.resource)

class Forest(ResourceSource):
    is_forest = True
    resource = 'pine'
    color = "darkgreen"

    def take_resource(self):
        if self.amount > 0:
            self.amount -= 1
        return Wood(self.resource)
