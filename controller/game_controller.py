import pygame
import sys
from view.main_menu_view import MainMenuView
from controller.main_menu_controller import MainMenuController
from view.world_view import WorldView
from controller.world_controller import WorldController


class GameController:
    def __init__(self, screen, game_data):
        self.screen = screen
        self.game_data = game_data
        self.current_state = None

    def run(self):
        self.change_state("main_menu")
        while True:
            if self.current_state == "main_menu":
                self.run_main_menu()
    def change_state(self, state):
        self.current_state = state

    def run_main_menu(self):
        view = MainMenuView(self.screen)
        controller = MainMenuController(self.game_data, view)  # Assume model is defined
        controller.run()
