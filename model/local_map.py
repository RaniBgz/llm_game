from model.map import Map

class LocalMap(Map):
    def __init__(self):
        super().__init__()
        self.items = []
        self.npcs = []
        self.dungeon_map = None  # Attribute to hold a nested dungeon map (if applicable)

    def add_player(self, character):
        self.player = character
        self.player.location = (0, 0)  # Set the character's location on this map

    def remove_player(self):
        self.player = None

    def is_dungeon(self):
        # Return True if this map is a dungeon, False otherwise
        return self.dungeon_map is not None

    def enter_dungeon(self):
        # If this map is a dungeon, transition to the dungeon map
        if self.is_dungeon():
            self.dungeon_map.add_player(self.player)
            self.player.change_map(self.dungeon_map)

    def exit_dungeon(self):
        # If the character is in a dungeon, transition back to the parent map
        if self.player.current_map is self.dungeon_map:
            self.remove_player()
            self.player.change_map(self.parent_map)