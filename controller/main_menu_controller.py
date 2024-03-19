import sys
import pygame
from view.main_game_view import MainGameView
from controller.main_game_controller import MainGameController

class MainMenuController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.view.play_rect.collidepoint(event.pos):
                        self.start_game()
                    elif self.view.quit_rect.collidepoint(event.pos):  # Add quit handling
                        pygame.quit()
                        sys.exit()

            self.view.display_menu()

    def start_game(self):
        # Transition to the main game
        game_view = MainGameView(self.view.screen)  # Reuse the screen
        game_controller = MainGameController(self.model, game_view)
        game_controller.run()
        # ... Logic to transition to MainGameController