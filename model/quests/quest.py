from model.entity import Entity
from model.quests.objective import Objective
import uuid

class Quest:
    def __init__(self, name, description, active):
        self.id = uuid.uuid4()
        self.name = name
        self.description = description
        self.active = active
        self.objectives = []

    def set_active(self, active):
        self.active = active

    def set_inactive(self):
        self.active = False