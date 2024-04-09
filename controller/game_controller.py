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
                print(f"Current state is: {self.current_state}")
                self.run_main_menu()
            elif self.current_state == "world":
                self.run_world()
            # Add more states as needed

    def change_state(self, state):
        self.current_state = state

    def run_main_menu(self):
        view = MainMenuView(self.screen)
        controller = MainMenuController(self.game_data, view)  # Assume model is defined
        controller.run()
        # Check for conditions to transition to the world view
        if controller.start_game:
            self.change_state("world")

    def run_world(self):
        world_view = WorldView(self.screen, [0, 0])  # Example position
        world_controller = WorldController(self.game_data, world_view)  # Assume model is defined
        world_controller.run()
        # Check for conditions to transition back to the main menu
        if world_controller.back_to_main_menu:
            self.change_state("main_menu")