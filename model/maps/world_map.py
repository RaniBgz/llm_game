from model.maps.local_map import LocalMap

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

    def build_map(self, x_size, y_size):
        for x in range(-x_size, x_size):
            for y in range(-y_size, y_size):
                print(f"Adding local map at {x}, {y}")
                self.map_grid[(x, y)] = LocalMap()

    def add_entity(self, entity, local_map_coords, local_position):
        local_map = self.map_grid[local_map_coords]
        local_map.add_entity(entity)

    def add_local_map(self, x, y, local_map):
        self.map_grid[(x, y)] = local_map

    def get_local_map_at(self, x, y):
        return self.map_grid[(x, y)]


    def set_player_coords(self, x, y):
        self.player_x = x
        self.player_y = y

    def get_player_coords(self):
        return self.player_x, self.player_y

    def add_npc_to_map(self, x, y, npc):
        local_map = self.get_local_map_at(x, y)
        if local_map:
            local_map.add_npc(npc)
