#!/usr/bin/env python3
from .human import Human


class HumanPeasant(Human):
    profession = 'peasant'

    def rest(self, loc, time):
        if len(self.short_memory.get('checked fields', [])) != \
           self.short_memory.get('fields count', -1):
            self.change_status('working')
            return


    def work(self, loc, time):
        if self.sub_status == None:
            self.change_sub_status('checking fields')
            self.long_memory['start location'] = loc


        if self.sub_status == 'checking fields':
            if len(self.short_memory.get('checked fields', [])) == \
               self.short_memory.get('fields count', -1):
                self.change_status('resting')
                self.go_to(self.long_memory['start location'])
                return


            if self.target is None or \
               not self.target.is_plantable or \
               self.target in self.short_memory.get('checked fields', []):
                self.change_sub_status('going to unchecked ground')
            else:
                self.go_to(self.target)
                for seed in self.target.seeds:
                    if seed.water < seed.water_multiplier * seed.value * seed.turns_to_grow * 1.1:
                        self.change_sub_status('watering')
                        self.short_memory['seeds to water'] = seed
                        return
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
                        checked = self.short_memory.get('checked fields', [])
                        checked.append(self.target)
                        self.short_memory['checked fields'] = checked
                        self.target = None
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

        if self.sub_status == 'watering':
            water = None
            water_ind = -1
            for ind, item in enumerate(self.inventory):
                if item.is_water:
                    water = item
                    water_ind = ind
            if water is not None:
                seeds = self.short_memory.get('seeds to water')
                if seeds is not None:
                    seeds.water += water.value
                    self.inventory.pop(water_ind)
                self.change_sub_status('checking fields')
            else:
                self.change_sub_status('getting water')


        if self.sub_status == 'getting water':
            if self.short_memory.get('water source') is None:
                for nloc in loc.locs:
                    if nloc.is_water_source:
                        self.short_memory['water source'] = nloc
            else:
                water = self.short_memory['water source'].get_water()
                self.inventory.append(water)
                self.change_sub_status('watering')


        if self.sub_status == 'going to unchecked ground':
            fields = 0
            for nloc in loc.locs:
                if nloc.is_plantable and \
                   nloc not in self.short_memory.get('checked fields', []):
                    fields += 1
            self.short_memory['fields count'] = fields
            for nloc in loc.locs:
                if nloc.is_plantable and \
                   nloc not in self.short_memory.get('checked fields', []):
                    self.target = nloc
                    self.change_sub_status('checking fields')
                    break

        if self.sub_status == 'gathering fruits':
            self.inventory.append(self.target.fruits[0])
            self.target.fruits.pop(0)
            if len(self.target.fruits) == 0:
                self.change_sub_status('checking fields')
