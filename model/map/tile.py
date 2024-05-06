import pygame
from view import view_constants as view_cst
from enum import Enum
class TileType(Enum):
    GRASS = 1
    SAND = 2

class Tile:
    def __init__(self, tile_type, image_path):
        self.type = tile_type  # Could be an Enum: TileType.GRASS, TileType.WATER, etc.
        self.image_path = image_path
        self.image = None
        self.monster = None  # Placeholder for future monster presence
        self.loot = None     # Placeholder for potential loot
        # ... add more attributes as needed (e.g., walkable, special properties)


    def load_image(self):
        # Load image from file
        self.image = pygame.image.load(self.image_path).convert_alpha()
        # Scale image to tile size
        self.image = pygame.transform.scale(self.image, (view_cst.TILE_WIDTH, view_cst.TILE_HEIGHT))

    # Later you can add methods like:
    def is_passable(self):
        # Logic based on tile type (e.g., water might not be passable)
        pass