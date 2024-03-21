from model.entity import Entity

class NPC(Entity):
    def __init__(self, name, hp):
        super().__init__()
        self.name = name
        self.hp = hp

    def get_id(self):
        return self.id

