import pygame
import view.view_constants as view_cst

class PygameTexture():
    def __init__(self, texture_path):
        self.texture_path = texture_path
        self.texture = self.load_texture() #Pygame surface

    def load_texture(self):
        image = pygame.image.load(self.texture_path).convert_alpha()
        # if self.texture_path == view_cst.CASTLE_ASSET_PATH:
        #     return pygame.transform.scale(image, (view_cst.TILE_WIDTH*3, view_cst.TILE_HEIGHT*2))
        return pygame.transform.scale(image, (view_cst.TILE_WIDTH, view_cst.TILE_HEIGHT))