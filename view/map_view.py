import sys
import pygame
from view import view_constants as view_cst

map_path = "assets/maps/world_map.png"

class MapView:
    def __init__(self, screen):
        self.screen = screen
        self.map_image = pygame.image.load(map_path).convert_alpha()
        self.back_button_text = pygame.font.SysFont("Arial", 20).render("Back", True, view_cst.TEXT_COLOR)
        self.back_button_rect = self.back_button_text.get_rect(topright=(view_cst.WIDTH - 10, 10))
        # self.back_button = pygame.Rect(self.back_button_rect.topleft, self.back_button_rect.size)

    def display_map(self):
        self.screen.fill(view_cst.WHITE)
        self.screen.blit(self.map_image, (0, 0))  # Assuming the map is the size of the screen
        self.screen.blit(self.back_button_text, self.back_button_rect)
        pygame.display.flip()
