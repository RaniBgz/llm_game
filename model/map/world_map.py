from model.map.local_map import LocalMap
from model.map.biome import Biome

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
        for x in range(0, x_size):
            for y in range(0, y_size):
                # XOR operation: True when one is odd and the other is even
                if (x + y) % 2 == 0:
                    self.map_grid[(x, y)] = LocalMap(biome=Biome.PLAIN)
                else:
                    self.map_grid[(x, y)] = LocalMap(biome=Biome.DESERT)

    def add_entity(self, entity, local_map_coords):
        local_map = self.map_grid[local_map_coords]
        local_map.add_entity(entity)
        print(f"Added entity {entity.name} to local map at {local_map_coords}")

    def remove_entity(self, entity, local_map_coords):
        local_map = self.map_grid[local_map_coords]
        local_map.remove_entity(entity)
        print(f"Removed entity {entity.name} from local map at {local_map_coords}")

    def add_local_map(self, x, y, local_map):
        self.map_grid[(x, y)] = local_map

    def get_local_map_at(self, x, y):
        return self.map_grid[(x, y)]

    def get_entities_at(self, x, y):
        local_map = self.map_grid[(x, y)]
        return local_map.entities

    def add_npc_to_map(self, x, y, npc):
        local_map = self.get_local_map_at(x, y)
        if local_map:
            local_map.add_npc(npc)
