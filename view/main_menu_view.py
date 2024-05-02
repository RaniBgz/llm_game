import pygame
from view import view_constants as view_cst
from view.ui.button import Button

import pygame
from view import view_constants as view_cst


class MainMenuView:
    def __init__(self, screen):
        self.screen = screen
        self.background_image = pygame.image.load("./assets/backgrounds/main_menu.png").convert()
        self.button_image = pygame.image.load("./assets/buttons/wood_button.png").convert_alpha()
        self.text_offset = 5

        self.title_font = pygame.font.SysFont("Arial", 50)
        self.button_font = pygame.font.SysFont("Arial", 30)
        self.title_text = self.title_font.render("Game Title", True, view_cst.DARK_GRAY_2)
        self.title_rect = self.title_text.get_rect(center=(view_cst.WIDTH / 2, view_cst.HEIGHT / 4))
        button_width = 300
        button_height = 100

        self.play_button = Button(self.button_image, self.button_font, button_width, button_height, self.text_offset,
                                  (view_cst.WIDTH / 2 - button_width/2, view_cst.HEIGHT / 2 - 100), "Play")
        self.quit_button = Button(self.button_image, self.button_font, button_width, button_height, self.text_offset,
                                  (view_cst.WIDTH / 2 - button_width/2, view_cst.HEIGHT / 2 + 50), "Quit")

    def display_menu(self):
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.title_text, self.title_rect)
        self.play_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        pygame.display.flip()