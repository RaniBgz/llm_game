import pygame
from view import view_constants as view_cst
from view.ui.button import Button

import pygame
from view import view_constants as view_cst


class MainMenuView:
    def __init__(self, screen):
        self.screen = screen
        self.width = view_cst.WIDTH
        self.height = view_cst.HEIGHT
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect()
        self.rect.topleft = (0, 0)
        self.background_image = pygame.image.load("./assets/backgrounds/main_menu.png").convert()
        self.default_button_image = pygame.image.load("./assets/buttons/wood_button.png").convert_alpha()
        self.default_pressed_button_image = pygame.image.load("./assets/buttons/wood_button_pressed.png").convert_alpha()
        self.text_offset = 5

        self.title_font = pygame.font.SysFont("Arial", 50)
        self.button_font = pygame.font.SysFont("Arial", 30)
        self.title_text = self.title_font.render("Game Title", True, view_cst.DARK_GRAY_2)
        self.title_rect = self.title_text.get_rect(center=(view_cst.WIDTH / 2, view_cst.HEIGHT / 4))
        button_width = 300
        button_height = 100

        self.play_button = Button(self.default_button_image, self.button_font, button_width, button_height, self.text_offset,
                                  (view_cst.WIDTH / 2 - button_width/2, view_cst.HEIGHT / 2 - 100), "Play",
                                  self.rect.topleft, pressed_image=self.default_pressed_button_image)
        self.quit_button = Button(self.default_button_image, self.button_font, button_width, button_height, self.text_offset,
                                  (view_cst.WIDTH / 2 - button_width/2, view_cst.HEIGHT / 2 + 50), "Quit",
                                  self.rect.topleft, pressed_image=self.default_pressed_button_image)

    def display_menu(self):
        self.surface.blit(self.background_image, (0, 0))
        self.surface.blit(self.title_text, self.title_rect)
        self.render_play_button()
        self.render_quit_button()
        self.screen.blit(self.surface, (0, 0))
        pygame.display.flip()

    def render_quit_button(self):
        self.quit_button.draw(self.surface)

    def render_play_button(self):
        self.play_button.draw(self.surface)

    def render_loading_screen(self):
        self.surface.fill(view_cst.BLACK)
        loading_text = pygame.font.SysFont("Arial", 30).render("Loading...", True, view_cst.WHITE)
        loading_rect = loading_text.get_rect(center=(view_cst.WIDTH / 2, view_cst.HEIGHT / 2))
        self.surface.blit(loading_text, loading_rect)
        self.screen.blit(self.surface, (0, 0))
        pygame.display.flip()