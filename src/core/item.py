class Item(object):
    name = None
    is_food = False
    is_weapon = False
    is_pickable = False
    is_interactable = True


    def __init__(self, position=None):
        self.in_inventory = False

    def use(self, target):
        pass

    def interact(self, target):
        pass


class Food(Item):
    is_food = True

    value = 0


class Cucumber(Food):
    name = 'cucumber'
