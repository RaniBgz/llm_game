import sys
import pygame
from view import view_constants as view_cst

class WorldView:
    def __init__(self, screen):
        self.screen = screen
        self.character_image = pygame.image.load("assets/sprites/character.png").convert_alpha()
        self.character_rect = self.character_image.get_rect(center=(view_cst.WIDTH // 2, view_cst.HEIGHT // 2))
        self.back_button_text = pygame.font.SysFont("Arial", 20).render("Back", True, view_cst.TEXT_COLOR)
        self.back_button_rect = self.back_button_text.get_rect(topright=(view_cst.WIDTH - 10, 10))

    def display_world(self):
        self.screen.fill(view_cst.WHITE)
        self.screen.blit(self.character_image, self.character_rect)
        self.screen.blit(self.back_button_text, self.back_button_rect)
        pygame.display.flip()

    def display_coordinates(self, x, y):
        # font = pygame.font.Font("Arial", 36)
        coord_text = pygame.font.SysFont("Arial", 20).render(f"({x}, {y})", True, view_cst.TEXT_COLOR)
        # coord_text = font.render(f"({x}, {y})", True, (255, 255, 255))
        coord_rect = coord_text.get_rect(topleft=(50, view_cst.HEIGHT - 10))
        # coord_rect.bottomleft = (10, view_cst.HEIGHT - 10)  # Position at bottom-left
        self.screen.blit(coord_text, coord_rect)