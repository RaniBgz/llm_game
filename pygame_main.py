import pygame
import sys
from view.main_menu_view import MainMenuView
from controller.main_menu_controller import MainMenuController
from model.game_model import GameModel

# Set up some constants
WIDTH, HEIGHT = 640, 480
WHITE = (255, 255, 255)
RED = (255, 0, 0)

def initialize_screen():
    # Initialize Pygame
    pygame.init()
    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    return screen


def main():
    screen = initialize_screen()
    model = GameModel()
    main_menu_view = MainMenuView(screen)
    main_menu_controller = MainMenuController(model, main_menu_view)
    main_menu_controller.run()

if __name__ == "__main__":
    main()
