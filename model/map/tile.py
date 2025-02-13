import pygame
from view import view_constants as view_cst
from view.asset.pygame_texture import PygameTexture

from enum import Enum
class TileType(Enum):
    GRASS = 1
    SAND = 2
    ROCK = 3
    PINE_TREE = 4
    FRIENDLY_HOUSE = 5
    HOSTILE_HOUSE = 6
    DUNGEON_ENTRANCE = 7
    CASTLE = 8
    TOWER = 9

class Tile:
    def __init__(self, layers, texture_manager):
        self.layers = layers #List of TileType enums
        self.textures = [texture_manager.get_texture(self.get_texture_path(layer)) for layer in layers]
        self.monster = None  # Placeholder for future monster presence
        self.loot = None     # Placeholder for potential loot
        # ... add more attributes as needed (e.g., walkable, special properties)

    def get_texture_path(self, tile_type):
        if tile_type == TileType.GRASS:
            return view_cst.GRASS_ASSET_PATH
        if tile_type == TileType.SAND:
            return view_cst.SAND_ASSET_PATH
        if tile_type == TileType.ROCK:
            return view_cst.ROCK_ASSET_PATH
        if tile_type == TileType.PINE_TREE:
            return view_cst.PINE_TREE_ASSET_PATH
        if tile_type == TileType.FRIENDLY_HOUSE:
            return view_cst.FRIENDLY_HOUSE_ASSET_PATH
        if tile_type == TileType.HOSTILE_HOUSE:
            return view_cst.HOSTILE_HOUSE_ASSET_PATH
        if tile_type == TileType.DUNGEON_ENTRANCE:
            return view_cst.DUNGEON_ENTRANCE_ASSET_PATH
        if tile_type == TileType.CASTLE:
            return view_cst.CASTLE_ASSET_PATH
        if tile_type == TileType.TOWER:
            return view_cst.TOWER_ASSET_PATH

    def draw(self, screen, position):
        for texture in self.textures:
            screen.blit(texture.texture, position)

    # def draw(self, screen, position):
    #     # Blit the tile texture at the given position on the screen
    #     screen.blit(self.texture.texture, position)

    # Later you can add methods like:
    def is_passable(self):
        # Logic based on tile type (e.g., water might not be passable)
        pass