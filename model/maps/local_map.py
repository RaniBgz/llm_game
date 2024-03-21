from model.maps.map import Map

class LocalMap(Map):
    def __init__(self):
        super().__init__()
        self.items = []
        self.npcs = []
        self.dungeon_map = None # Attribute to hold a nested dungeon map (if applicable)
        self.parent_map = None

    def add_player(self, character):
        self.player = character
        self.player.location = (0, 0)  # Set the character's location on this map

    def remove_player(self):
        self.player = None
