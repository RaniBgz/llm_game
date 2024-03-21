from model.entity import Entity

class NPC(Entity):
    def __init__(self, name, hp):
        super().__init__()
        self.name = name
        self.hp = hp
        self.current_map = None

    def get_id(self):
        return self.id

    def set_location(self, map, x, y):
        self.current_map = map
        self.x = x
        self.y = y
