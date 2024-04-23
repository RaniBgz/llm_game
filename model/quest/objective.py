import uuid

class Objective:
    def __init__(self, name: str, description: str):
        self.id = uuid.uuid4()
        self.name = name
        self.description = description
        self.completed = False

    def set_completed(self) -> None:
        self.completed = True

    def set_not_completed(self) -> None:
        self.completed = False


class KillObjective(Objective):
    def __init__(self, name: str, description: str, target_id: uuid.UUID):
        super().__init__(name, description)
        self.target_id = target_id

class LocationObjective(Objective):
    def __init__(self, name: str, description: str, target_location: str):
        super().__init__(name, description)
        self.target_location = target_location

class RetrievalObjective(Objective):
    def __init__(self, name: str, description: str, target_item_id: uuid.UUID):
        super().__init__(name, description)
        self.target_item_id = target_item_id

class TalkToNPCObjective(Objective):
    def __init__(self, name: str , description: str, target_npc_id: uuid.UUID):
        super().__init__(name, description)
        self.target_npc_id = target_npc_id

