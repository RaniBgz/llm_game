import pygame
from model.map.map import Map
from view import view_constants as view_cst
from model.map.biome import Biome
from model.map.tile import Tile, TileType

class LocalMap(Map):


    def __init__(self):
        super().__init__()
        self.entities = []
        self.tile_grid = [[None for _ in range(view_cst.V_TILES)] for _ in range(view_cst.H_TILES)]
        # Initialize grass tiles
        # tile_image = pygame.image.load("./assets/maps/tiles/grass.png").convert_alpha()
        self.grass_tile = Tile(TileType.GRASS, "./assets/maps/tiles/grass.png")
        self.sand_tile = Tile(TileType.SAND, "./assets/maps/tiles/sand.png")
        self.initialize_tiles()
        # self.grass_tile = pygame.transform.scale(self.grass_tile.image, (view_cst.TILE_WIDTH, view_cst.TILE_HEIGHT))

    def initialize_tiles(self):
        for i in range(view_cst.H_TILES):
            for j in range(view_cst.V_TILES):
                self.tile_grid[i][j] = self.grass_tile


    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)