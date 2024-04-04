import pygame
from view import view_constants as view_cst
from view.ui.button import Button

import pygame
from view import view_constants as view_cst

#TODO: Fix buttons hitboxes
class MainMenuView:
    def __init__(self, screen):
        self.screen = screen
        self.background_image = pygame.image.load("./assets/backgrounds/main_menu.png").convert()
        self.button_image = pygame.image.load("./assets/buttons/wood_button.png").convert_alpha()

        self.title_font = pygame.font.SysFont("Arial", 50)
        self.title_text = self.title_font.render("Game Title", True, view_cst.DARK_GRAY_2)
        self.title_rect = self.title_text.get_rect(center=(view_cst.WIDTH / 2, view_cst.HEIGHT / 4))

        self.play_button = Button(self.button_image, (view_cst.WIDTH / 2, view_cst.HEIGHT / 2), "Play")
        self.quit_button = Button(self.button_image, (view_cst.WIDTH / 2, view_cst.HEIGHT / 2 + 100), "Quit")

    def display_menu(self):
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.title_text, self.title_rect)
        self.play_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        pygame.display.flip()



# class MainMenuView:
#     def __init__(self, screen):
#         self.screen = screen
#         self.title_font = pygame.font.SysFont("Arial", 50)
#         self.title_text = self.title_font.render("Game Title", True, view_cst.TEXT_COLOR)
#         self.title_rect = self.title_text.get_rect(center=(view_cst.WIDTH / 2, view_cst.HEIGHT / 4))
#
#         self.play_font = pygame.font.SysFont("Arial", 30)
#         self.play_text = self.play_font.render("Play", True, view_cst.TEXT_COLOR)
#         self.play_rect = self.play_text.get_rect(center=(view_cst.WIDTH / 2, view_cst.HEIGHT / 2))
#
#         self.quit_font = pygame.font.SysFont("Arial", 30)
#         self.quit_text = self.quit_font.render("Quit", True, view_cst.TEXT_COLOR)
#         self.quit_rect = self.quit_text.get_rect(center=(view_cst.WIDTH / 2, view_cst.HEIGHT / 2 + 50))
#
#
#     def display_menu(self):
#         self.screen.fill(view_cst.WHITE)
#         self.screen.blit(self.title_text, self.title_rect)
#         self.screen.blit(self.play_text, self.play_rect)
#         self.screen.blit(self.quit_text, self.quit_rect)
#         pygame.display.flip()
#
#
#     def handle_event(self, event):
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if self.play_rect.collidepoint(event.pos):
#                 pass

