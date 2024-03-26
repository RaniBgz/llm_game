from model.maps.map import Map

class LocalMap(Map):
    def __init__(self):
        super().__init__()
        self.items = []
        self.entities = []
        self.parent_map = None

    def add_player(self, character):
        self.player = character
        self.player.location = (0, 0)  # Set the character's location on this map

    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_player(self):
        self.player = None
