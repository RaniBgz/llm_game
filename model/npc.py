from model.entity import Entity

default_sprite = "./assets/default.png"

class NPC(Entity):
    def __init__(self, name, hp, sprite=default_sprite):
        super().__init__()
        self.name = name
        self.hp = hp
        self.sprite = sprite
        self.current_map = None

    def get_id(self):
        return self.id

    def set_location(self, map, x, y):
        self.current_map = map
        self.x = x
        self.y = y

    def set_sprite(self, sprite):
        self.sprite = sprite
