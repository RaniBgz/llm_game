from model.entity import Entity
from model.quest.objective import Objective
import uuid


class Quest:
    def __init__(self, name: str,
                 description: str,
                 ordered: bool = False,
                 active: bool = False,
                 completed: bool = False,
                 ended: bool = False):
        self.id = uuid.uuid4()
        self.name = name
        self.description = description
        self.ordered = ordered
        self.active = active
        self.completed = completed
        self.ended = ended
        if ordered:
            self.current_objective = 0
        else:
            self.current_objective = -1
        self.objectives = []

    def get_id(self):
        return self.id

    def get_objectives(self):
        return self.objectives

    def get_current_objective(self):
        if self.ordered:
            return self.objectives[self.current_objective]
        else:
            return self.objectives[0]

    def point_to_next_objective(self):
        if self.ordered:
            if self.current_objective == len(self.objectives) - 1:
                self.completed = True
                return False
            else:
                self.current_objective += 1

    def check_all_objectives_completed(self):
        for objective in self.objectives:
            if not objective.completed:
                return False
        self.completed = True
        return True

    def add_objective(self, objective):
        self.objectives.append(objective)

    def remove_objective(self, objective):
        self.objectives.remove(objective)

    def set_active(self):
        self.active = True

    def set_inactive(self):
        self.active = False

    def set_completed(self):
        self.completed = True

    def set_not_completed(self):
        self.completed = False
        if self.ordered:
            self.current_objective = 0

    def set_ended(self):
        self.ended = True

    def set_not_ended(self):
        self.ended = False

    def set_not_completed(self):
        self.completed = False
        if self.ordered:
            self.current_objective = 0
