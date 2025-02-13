from model.entity import Entity
from model.subject.subject import Subject

default_sprite = "./assets/default.png"

class Item(Entity, Subject):
    def __init__(self, name,
                 description,
                 sprite=default_sprite,
                 global_position=(0, 0),
                 local_position=(0, 0),
                 in_world=False,
                 embedding=None):
        Entity.__init__(self)
        Subject.__init__(self)
        self.name = name
        self.description = description
        self.sprite = sprite
        self.global_position = global_position
        self.local_position = local_position
        self.in_world = in_world
        self.embedding = embedding
        self.initial_state = {"global_position": global_position,
                              "local_position": local_position,
                              "in_world": in_world}

    def notify(self, *args, **kwargs):
        # print(f"Notifying with args[1]: {args[1]}")
        for observer in self._observers:
            observer.update(self, *args, **kwargs)


    '''Getter for ID of the item.'''
    def get_id(self):
        return self.id


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

    def set_in_world(self):
        self.in_world = True
        self.notify(self, "item_added_to_world")

    def set_in_inventory(self):
        self.in_world = False
        self.notify(self, "item_removed_from_world")

    def reset_item(self):
        print(f"Initial state: {self.initial_state}")
        if self.global_position != self.initial_state["global_position"]:
            self.global_position = self.initial_state["global_position"]
        if self.local_position != self.initial_state["local_position"]:
            self.local_position = self.initial_state["local_position"]
        if self.in_world != self.initial_state["in_world"]:
            self.in_world = self.initial_state["in_world"]
            if self.in_world:
                self.notify(self, "item_added_to_world")
            else:
                self.notify(self, "item_removed_from_world")
