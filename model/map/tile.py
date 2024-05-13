import pygame
from view import view_constants as view_cst
from view.asset.pygame_texture import PygameTexture

from enum import Enum
class TileType(Enum):
    GRASS = 1
    SAND = 2
    ROCK = 3
    FRIENDLY_HOUSE = 4
    HOSTILE_HOUSE = 5

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
        image = pygame.image.load(self.image_path).convert_alpha()
        # Scale image to tile size
        self.image = pygame.transform.scale(image, (view_cst.TILE_WIDTH, view_cst.TILE_HEIGHT))
        return image

    # Later you can add methods like:
    def is_passable(self):
        # Logic based on tile type (e.g., water might not be passable)
        pass