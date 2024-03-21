import pygame
from view.main_menu_view import MainMenuView
from controller.main_menu_controller import MainMenuController
from model.game_data import GameData
from model.character import Character
from model.item import Item
from model.quests.quest import Quest
from model.settings import Settings
from view import view_constants as view_cst
from model.maps.world_map import WorldMap

#TODO: find a place to store that

def initialize_screen():
    # Initialize Pygame
    pygame.init()
    # Set up the display
    screen = pygame.display.set_mode((view_cst.WIDTH, view_cst.HEIGHT))
    return screen



def initialize_character():
    return Character(16)

def main():
    WorldMap()
    world_map = WorldMap.get_instance()
    world_map.set_player_coords(0, 0)
    model = GameData()
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
