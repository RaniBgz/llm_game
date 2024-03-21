from model.entity import Entity
from model.quests.objective import Objective

class Quest:
    def __init__(self, name, description, active):
        self.name = name
        self.description = description
        self.active = active
        self.objective = None