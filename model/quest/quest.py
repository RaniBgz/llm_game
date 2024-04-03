from model.entity import Entity
from model.quest.objective import Objective
import uuid

class Quest:
    def __init__(self, name, description, ordered=False, active=False, completed=False):
        self.id = uuid.uuid4()
        self.name = name
        self.description = description
        self.ordered = ordered
        self.active = active
        self.completed = completed
        if ordered:
            current_objective = 0
        else:
            current_objective = -1
        self.objectives = []

    def set_active(self, active):
        self.active = active

    def set_inactive(self):
        self.active = False