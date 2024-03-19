import pygame
import sys
from view.main_menu_view import MainMenuView
from controller.main_menu_controller import MainMenuController
from model.game_model import GameModel
from model.character import Character
from model.item import Item
from model.quest import Quest
from model.settings import Settings
from view import view_constants as view_cst



#TODO: find a place to store that

def initialize_screen():
    # Initialize Pygame
    pygame.init()
    # Set up the display
    screen = pygame.display.set_mode((view_cst.WIDTH, view_cst.HEIGHT))
    return screen


def main():
    model = GameModel()
    settings = Settings()
    screen = initialize_screen()
    model.character = Character(16)  # Create a character
    model.character.add_item_to_inventory(Item("Sword", "A Rusty Sword"))
    model.character.add_item_to_inventory(Item("Healing Potion", "Restores Health"))

    model.character.add_quest(Quest("Defeat the Goblin", "Find and defeat the Goblin King", True))
    model.character.add_quest(Quest("Find the Hidden Treasure", "Follow the clues...", False))

    main_menu_view = MainMenuView(screen)
    main_menu_controller = MainMenuController(model, main_menu_view)
    main_menu_controller.run()

if __name__ == "__main__":
    main()
