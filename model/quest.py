from model.entity import Entity

class Quest:
    def __init__(self, name, description, active):
        super().__init__()
        self.name = name
        self.description = description
        self.active = active