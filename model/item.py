from model.entity import Entity

default_sprite = "./assets/default.png"

class Item(Entity):
    def __init__(self, name, description, sprite=default_sprite, global_position=(0, 0), local_position=(0, 0), in_world=False,):
        super().__init__()
        self.name = name
        self.description = description
        self.sprite = None
        self.global_position = global_position
        self.local_position = local_position
        self.in_world = False

    '''Setters for global and local positions of the item.'''
    def set_global_position(self, x, y):
        self.global_position = (x, y)

    def set_local_position(self, x, y):
        self.local_position = (x, y)

    '''Getters for global and local positions of the item.'''
    def get_global_x(self):
        return self.global_position[0]

    def get_global_y(self):
        return self.global_position[1]

    def get_local_x(self):
        return self.local_position[0]

    def get_local_y(self):
        return self.local_position[1]


