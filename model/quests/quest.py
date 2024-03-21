from model.entity import Entity

class Quest:
    def __init__(self, name, description, active):
        self.name = name
        self.description = description
        self.active = active
        self.objective = None