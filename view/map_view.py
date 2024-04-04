import sys
import pygame
from view import view_constants as view_cst

map_path = "assets/maps/world_map.png"

class MapView:
    def __init__(self, screen):
        self.screen = screen
        self.map_image = pygame.image.load(map_path).convert_alpha()
        self.map_image = pygame.transform.scale(self.map_image, (view_cst.WIDTH, view_cst.HEIGHT))
        self.exit_font = pygame.font.SysFont("Arial", 30)
        self.back_button_text = self.exit_font.render("Back", True, view_cst.TEXT_COLOR)
        self.back_button_rect = self.back_button_text.get_rect(topright=(view_cst.WIDTH - 10, 10))

    def display_map(self):
        self.screen.fill(view_cst.WHITE)
        self.screen.blit(self.map_image, (0, 0))
        self.screen.blit(self.back_button_text, self.back_button_rect)
        pygame.display.flip()
