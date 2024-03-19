from model.map import Map

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

    def set_player_coords(self, x, y):
        self.player_x = x
        self.player_y = y

    def get_player_coords(self):
        return self.player_x, self.player_y


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
    # def set_player_coords(self, x, y):
    #     self.player_x = x
    #     self.player_y = y
    #
    # def get_player_coords(self):
    #     return self.player_x, self.player_y