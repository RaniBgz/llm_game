from model.entity import Entity

class Item(Entity):
    def __init__(self, name, description):
        super().__init__()
        self.name = name
        self.description = description