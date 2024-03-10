from model.entity import Entity

class Item(Entity):
    def __init__(self, name, description, value, weight):
        super().__init__(name, description)
        self.value = value
        self.weight = weight