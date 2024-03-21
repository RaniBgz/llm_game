class WorldMap():
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(WorldMap, cls).__new__(cls, *args, **kwargs)
            # Initialize any variables here if needed
            cls._instance.map_grid = {}  # Use a dictionary for coordinate-based lookup
        return cls._instance
    def __init__(self):
        if "map_grid" not in self.__dict__:
            self.map_grid = {}  # Ensure this only happens once

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = WorldMap()
        return cls._instance

    def add_local_map(self, x, y, local_map):
        self.map_grid[(x, y)] = local_map

    def get_local_map_at(self, x, y):
        return self.map_grid[(x, y)]

    def set_player_coords(self, x, y):
        self.player_x = x
        self.player_y = y

    def get_player_coords(self):
        return self.player_x, self.player_y


    # def get_player_coords(self):
    #     return self.get_current_map().get_player_coords()
    #
    # def set_player_coords(self, x, y):
    #     self.get_current_map().set_player_coords(x, y)

    # def get_current_map(self):
    #     return self.get_local_map_at(self.get_player_x(), self.get_player_y())
    #
    # def set_current_map(self, new_map):
    #     # If the new map is not None, the character is moving to a new map
    #     if new_map is not None:
    #         self.get_local_map_at(self.get_player_x(), self.get_player_y()).remove_player()
    #         new_map.add_player(self)
    #         self.current_map = new_map
    #
    # def get_player_x(self):
    #     return self.current_map.get_player_x()
    #
    # def get_player_y(self):
    #     return self.current_map.get_player_y()
    #
    # def transition_player(self, current_map, new_x, new_y, target_map=None):
    #     current_map.remove_player()  # Remove from the current map
    #
    #     if target_map is None:
    #         # Transition on the overworld
    #         self.add_local_map(new_x, new_y, self.get_local_map_at(new_x, new_y))
    #     else:
    #         # Enter a submap
    #         target_map.add_player(self.player)
    #
    #     self.player.change_map(target_map)  # Update the player's location

    # def set_player_coords(self, x, y):
    #     self.player_x = x
    #     self.player_y = y
    #



    # def __init__(self):
    #     if WorldMap._instance is not None:
    #         raise Exception("Singleton cannot be instantiated twice!")
    #     self.map_grid = {}  # Use a dictionary for coordinate-based lookup
    #     self._instance = self
    #
    # @staticmethod
    # def get_instance():
    #     if WorldMap._instance is None:
    #         WorldMap()
    #     return WorldMap._instance
    #

    # def get_player_coords(self):
    #     return self.player_x, self.player_y