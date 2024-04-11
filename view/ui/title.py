import pygame
import view_constants as view_cst


class Title:
    def __init__(self, screen, title, font_size=32):
        self.screen = screen
        self.title_font = pygame.font.SysFont("Arial", font_size)
        self.title_text = self.title_font.render(title, True, view_cst.TEXT_COLOR)
        self.title_rect = self.title_text.get_rect(center=(view_cst.WIDTH // 2, 40))

    def display(self):
        self.screen.blit(self.title_text, self.title_rect)
        pygame.display.flip()