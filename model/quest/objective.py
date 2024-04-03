import uuid

class Objective:
    def __init__(self, name, description):
        self.id = uuid.uuid4()
        self.name = name
        self.description = description
        self.completed = False

    def set_completed(self):
        self.completed = True

    def set_not_completed(self):
        self.completed = False


class KillObjective(Objective):
    def __init__(self, name, description, target_id):
        super().__init__(name, description)
        self.target_id = target_id


class LocationObjective(Objective):
    def __init__(self, name, description, target_location):
        super().__init__(name, description)
        self.target_location = target_location


class RetrievalObjective(Objective):
    def __init__(self, name, description, target_item_id):
        super().__init__(name, description)
        self.target_item_id = target_item_id


class TalkToNPCObjective(Objective):
    def __init__(self, name, description, target_npc_id):
        super().__init__(name, description)
        self.target_npc_id = target_npc_id

