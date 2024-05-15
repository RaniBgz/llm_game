import pygame
from model.map.map import Map
from view import view_constants as view_cst
from model.map.biome import Biome
from model.map.tile import Tile, TileType

class LocalMap(Map):


    def __init__(self, texture_manager, biome=Biome.PLAIN):
        super().__init__()
        self.texture_manager = texture_manager
        self.entities = []
        self.biome = biome
        self.region_name = ""
        self.tile_grid = [[None for _ in range(view_cst.V_TILES)] for _ in range(view_cst.H_TILES)]
        # Initialize grass tiles
        # tile_image = pygame.image.load("./assets/maps/tiles/grass.png").convert_alpha()
        if self.biome == Biome.PLAIN:
            self.initialize_plain_biome()
        elif self.biome == Biome.DESERT:
            self.initialize_desert_biome()
        elif self.biome == Biome.MOUNTAIN:
            self.initialize_mountain_biome()
        elif self.biome == Biome.VILLAGE:
            self.initialize_village_biome()
        elif self.biome == Biome.FOREST:
            self.initialize_forest_biome()
        elif self.biome == Biome.HOSTILE_CAMP:
            self.initialize_hostile_camp()
        elif self.biome == Biome.DUNGEON:
            self.initialize_dungeon_biome()

        # self.initialize_tiles()
        # self.grass_tile = pygame.transform.scale(self.grass_tile.image, (view_cst.TILE_WIDTH, view_cst.TILE_HEIGHT))

    def initialize_plain_biome(self):
        for i in range(view_cst.H_TILES):
            for j in range(view_cst.V_TILES):
                grass_tile = Tile([TileType.GRASS], self.texture_manager)
                self.tile_grid[i][j] = grass_tile

    def initialize_desert_biome(self):
        for i in range(view_cst.H_TILES):
            for j in range(view_cst.V_TILES):
                sand_tile = Tile([TileType.SAND], self.texture_manager)
                self.tile_grid[i][j] = sand_tile

    def initialize_mountain_biome(self):
        for i in range(view_cst.H_TILES):
            for j in range(view_cst.V_TILES):
                rock_tile = Tile([TileType.ROCK], self.texture_manager)
                self.tile_grid[i][j] = rock_tile

    def initialize_village_biome(self):
        for i in range(view_cst.H_TILES):
            for j in range(view_cst.V_TILES):
                if (i==view_cst.H_TILES//2 - 2) or (i==view_cst.H_TILES//2 + 1):
                    if view_cst.V_TILES //3 <=j<=2*view_cst.V_TILES //3-1:
                        house_tile = Tile([TileType.GRASS, TileType.FRIENDLY_HOUSE], self.texture_manager)
                        self.tile_grid[i][j] = house_tile
                    else:
                        grass_tile = Tile([TileType.GRASS], self.texture_manager)
                        self.tile_grid[i][j] = grass_tile
                else:
                    grass_tile = Tile([TileType.GRASS], self.texture_manager)
                    self.tile_grid[i][j] = grass_tile

    def initialize_forest_biome(self):
        for i in range(view_cst.H_TILES):
            for j in range(view_cst.V_TILES):
                if  view_cst.H_TILES // 2 - 2 <= i <= view_cst.H_TILES // 2 + 1:
                    if view_cst.V_TILES // 3 <= j <= 2 * view_cst.V_TILES // 3 - 1:
                        pine_tree_tile = Tile([TileType.GRASS, TileType.PINE_TREE], self.texture_manager)
                        self.tile_grid[i][j] = pine_tree_tile
                    else:
                        grass_tile = Tile([TileType.GRASS], self.texture_manager)
                        self.tile_grid[i][j] = grass_tile
                else:
                    grass_tile = Tile([TileType.GRASS], self.texture_manager)
                    self.tile_grid[i][j] = grass_tile

    def initialize_hostile_camp(self):
        for i in range(view_cst.H_TILES):
            for j in range(view_cst.V_TILES):
                if (i==view_cst.H_TILES//2 - 2) or (i==view_cst.H_TILES//2 + 1):
                    if view_cst.V_TILES //3 <=j<=2*view_cst.V_TILES //3-1:
                        hostile_house_tile = Tile([TileType.GRASS, TileType.HOSTILE_HOUSE], self.texture_manager)
                        self.tile_grid[i][j] = hostile_house_tile
                    else:
                        grass_tile = Tile([TileType.GRASS], self.texture_manager)
                        self.tile_grid[i][j] = grass_tile
                else:
                    grass_tile = Tile([TileType.GRASS], self.texture_manager)
                    self.tile_grid[i][j] = grass_tile

    def initialize_dungeon_biome(self):
        for i in range(view_cst.H_TILES):
            for j in range(view_cst.V_TILES):
                if i==view_cst.H_TILES//2 - 1:
                    if j==view_cst.V_TILES//2 - 2:
                        dungeon_entrance_tile = Tile([TileType.ROCK, TileType.DUNGEON_ENTRANCE], self.texture_manager)
                        self.tile_grid[i][j] = dungeon_entrance_tile
                    else:
                        rock_tile = Tile([TileType.ROCK], self.texture_manager)
                        self.tile_grid[i][j] = rock_tile
                else:
                    rock_tile = Tile([TileType.ROCK], self.texture_manager)
                    self.tile_grid[i][j] = rock_tile

    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)