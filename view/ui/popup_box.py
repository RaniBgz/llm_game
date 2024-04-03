import abc
import pygame
from view import view_constants as view_cst

class PopupBox(abc.ABC):
    def __init__(self, screen, width, height):
        print(f"In popup constructor")
        self.screen = screen
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect()
        self.exit_font = pygame.font.SysFont("Arial", 32)
        # self.close_button_rect = None
        self.show = False

    @abc.abstractmethod
    def handle_events(self, event):
        pass

    def display(self):
        if self.show:
            self.screen.blit(self.surface, self.rect)

    def set_position(self, position):
        self.rect.topleft = position
