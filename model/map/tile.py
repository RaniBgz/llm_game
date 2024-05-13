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
    def __init__(self, tile_type, texture_manager):
        self.tile_type = tile_type  # Could be an Enum: TileType.GRASS, TileType.WATER, etc.
        self.texture = texture_manager.get_texture(self.get_texture_path())
        self.image = None
        self.monster = None  # Placeholder for future monster presence
        self.loot = None     # Placeholder for potential loot
        # ... add more attributes as needed (e.g., walkable, special properties)

    def get_texture_path(self):
        if self.tile_type == TileType.GRASS:
            return view_cst.GRASS_ASSET_PATH
        elif self.tile_type == TileType.SAND:
            return view_cst.SAND_ASSET_PATH
        elif self.tile_type == TileType.ROCK:
            return view_cst.ROCK_ASSET_PATH
        elif self.tile_type == TileType.FRIENDLY_HOUSE:
            return view_cst.FRIENDLY_HOUSE_ASSET_PATH
        elif self.tile_type == TileType.HOSTILE_HOUSE:
            return view_cst.HOSTILE_HOUSE_ASSET_PATH

    # def load_image(self):
    #     # Load image from file
    #     image = pygame.image.load(self.image_path).convert_alpha()
    #     # Scale image to tile size
    #     self.image = pygame.transform.scale(image, (view_cst.TILE_WIDTH, view_cst.TILE_HEIGHT))
    #     return image

    def draw(self, screen, position):
        # Blit the tile texture at the given position on the screen
        screen.blit(self.texture.texture, position)

    # Later you can add methods like:
    def is_passable(self):
        # Logic based on tile type (e.g., water might not be passable)
        pass