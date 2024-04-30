import sys
import pygame
from view.world_view import WorldView
from controller.world_controller import WorldController

class MainMenuController:
    def __init__(self, game_data, view):
        self.game_data = game_data
        self.view = view

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # self.view.play_button.handle_events(event)
                    # self.view.quit_button.handle_events(event)
                    if self.view.play_button.rect.collidepoint(event.pos):
                        #TODO: Instead of starting game from the main menu, update the observer (game controller) and let it handle the transition
                        print(f"Rect position: {self.view.play_button.rect.topleft}")
                        self.start_game()
                    elif self.view.quit_button.rect.collidepoint(event.pos):  # Add quit handling
                        print(f"Rect position: {self.view.quit_button.rect.topleft}")
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    pass
                    # self.view.play_button.handle_events(event)
                    # self.view.quit_button.handle_events(event)

            self.view.display_menu()

    def start_game(self):
        # Transition to the main game
        world_view = WorldView(self.view.screen, self.game_data.character.global_position)
        world_controller = WorldController(self.game_data, self, world_view)
        world_controller.run()
