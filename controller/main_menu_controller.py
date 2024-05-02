import sys
import pygame
from view.world_view import WorldView
from controller.world_controller import WorldController

class MainMenuController:
    def __init__(self, game_data, view):
        self.game_data = game_data
        self.view = view
        self.button_flags = {
            "play": False,
            "quit": False
        }

    def run(self):
        while True:
            self.view.display_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_events(event)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down_event(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up_event(event)

    def handle_mouse_down_event(self, event):
        if getattr(self.view, 'quit_button', None):
            if self.view.quit_button.is_clicked(event):
                self.view.quit_button.handle_mouse_down()
                self.button_flags["quit"] = True
        if getattr(self.view, 'play_button', None):
            if self.view.play_button.is_clicked(event):
                self.view.play_button.handle_mouse_down()
                self.button_flags["play"] = True

    def handle_mouse_up_event(self, event):
        if getattr(self.view, 'quit_button', None):
            self.view.quit_button.handle_mouse_up()
            if self.view.quit_button.is_clicked(event):
                if self.button_flags["quit"]:
                    pygame.quit()
                    sys.exit()
        if getattr(self.view, 'play_button', None):
            self.view.play_button.handle_mouse_up()
            if self.view.play_button.is_clicked(event):
                if self.button_flags["play"]:
                    self.view.render_loading_screen()
                    self.start_game()

    def start_game(self):
        # Transition to the main game
        world_view = WorldView(self.view.screen, self.game_data.character.global_position)
        world_controller = WorldController(self.game_data, self, world_view)
        world_controller.run()
