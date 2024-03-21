class Objective:
    def __init__(self):
        pass

    def check_completion(self, player):
        raise NotImplementedError("Subclasses must implement check_completion!")


class KillObjective(Objective):
    def __init__(self, target_id):
        super().__init__()
        self.target_id = target_id

    def check_completion(self, player):
        # Logic to check if the entity with target_id has been killed by the player
        pass


class LocationObjective(Objective):
    def __init__(self, target_location):
        super().__init__()
        self.target_location = target_location

    def check_completion(self, player):
        # Logic to check if the player is at the target_location
        pass


class RetrievalObjective(Objective):
    def __init__(self, target_item_id):
        super().__init__()
        self.target_item_id = target_item_id

    def check_completion(self, player):
        # Logic to check if the target_item_id is in the player's inventory.
        pass