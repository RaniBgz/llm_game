from model.map.local_map import LocalMap
from model.map.biome import Biome
from view.asset.texture_manager import TextureManager

class WorldMap():
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(WorldMap, cls).__new__(cls, *args, **kwargs)
            # Initialize any variables here if needed
            cls._instance.map_grid = {}  # Use a dictionary for coordinate-based lookup
            cls._instance.x_size = 0
            cls._instance.y_size = 0
            cls._instance.texture_manager = TextureManager()
        return cls._instance
    def __init__(self):
        if "map_grid" not in self.__dict__:
            self.map_grid = {}  # Ensure this only happens once
            self.x_size = 0
            self.y_size = 0
            self.texture_manager = TextureManager()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = WorldMap()
        return cls._instance

    def build_map(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        for x in range(0, x_size):
            for y in range(0, y_size):
                # XOR operation: True when one is odd and the other is even
                if x==2 and y==3:
                    self.map_grid[(x, y)] = LocalMap(self.texture_manager, biome=Biome.DUNGEON)
                elif x==3 and y==3:
                    self.map_grid[(x, y)] = LocalMap(self.texture_manager, biome=Biome.VILLAGE)
                elif x==4 and y==3:
                    self.map_grid[(x, y)] = LocalMap(self.texture_manager, biome=Biome.FOREST)
                elif x==3 and y==4:
                    self.map_grid[(x, y)] = LocalMap(self.texture_manager, biome=Biome.HOSTILE_CAMP)
                elif (x + y) % 3 == 0:
                    self.map_grid[(x, y)] = LocalMap(self.texture_manager, biome=Biome.DESERT)
                elif (x + y) % 3 == 1:
                    self.map_grid[(x, y)] = LocalMap(self.texture_manager, biome=Biome.PLAIN)
                else:
                    self.map_grid[(x, y)] = LocalMap(self.texture_manager, biome=Biome.MOUNTAIN)

    def get_context(self):
        context_parts = []
        context_parts.append(f"World Map Size: {self.x_size}x{self.y_size}")
        for (x, y), local_map in self.map_grid.items():
            biome_name = local_map.biome.name
            region_name = local_map.region_name if local_map.region_name else ""
            context_parts.append(f"Region ({x}, {y}): {biome_name} {region_name}")
        context_string = " | ".join(context_parts)
        return context_string

    def add_entity(self, entity, local_map_coords):
        local_map = self.map_grid[local_map_coords]
        local_map.add_entity(entity)
        # print(f"Added entity {entity.name} to local map at {local_map_coords}")

    def remove_entity(self, entity, local_map_coords):
        local_map = self.map_grid[local_map_coords]
        local_map.remove_entity(entity)
        # print(f"Removed entity {entity.name} from local map at {local_map_coords}")

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
