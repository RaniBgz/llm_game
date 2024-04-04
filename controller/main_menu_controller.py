import sys
import pygame
from view.main_game_view import MainGameView
from controller.main_game_controller import MainGameController
from view.world_view import WorldView
from controller.world_controller import WorldController

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
                    if self.view.play_button.rect.collidepoint(event.pos):
                        print(f"Rect position: {self.view.play_button.rect.topleft}")
                        self.start_game()
                    elif self.view.quit_button.rect.collidepoint(event.pos):  # Add quit handling
                        print(f"Rect position: {self.view.quit_button.rect.topleft}")
                        pygame.quit()
                        sys.exit()

            self.view.display_menu()

    def start_game(self):
        # Transition to the main game
        world_view = WorldView(self.view.screen, self.model.character.global_position)
        world_controller = WorldController(self.model, world_view)
        world_controller.run()
