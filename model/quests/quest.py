from model.entity import Entity
from model.quests.objective import Objective

class Quest:
    def __init__(self, name, description, active):
        self.name = name
        self.description = description
        self.active = active
        self.objective = None

    def set_active(self, active):
        self.active = active

    def set_inactive(self):
        self.active = False