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

class Game:
    def __init__(self, screen_width, screen_height):
        self.screen = None  # Initialize screen later in setup
        self.model = GameData()
        self.settings = Settings(screen_width, screen_height)

    def setup(self):
        world_map = WorldMap.get_instance()
        world_map.set_player_coords(0, 0)
        self.initialize_character()
        self.screen = self.initialize_screen()


    def initialize_character(self):
        self.model.character = Character(16)
        self.model.character.add_item_to_inventory(Item("Sword", "A Rusty Sword"))
        self.model.character.add_item_to_inventory(Item("Healing Potion", "Restores Health"))
        self.model.character.add_quest(Quest("Defeat the Goblin", "Find and defeat the Goblin King", True))
        self.model.character.add_quest(Quest("Find the Hidden Treasure", "Follow the clues...", False))
        return Character(16)

    def initialize_screen(self):
        pygame.init()
        screen = pygame.display.set_mode((view_cst.WIDTH, view_cst.HEIGHT))
        return screen

    def initialize_ui(self):
        main_menu_view = MainMenuView(self.screen)
        main_menu_controller = MainMenuController(self.model, main_menu_view)
        main_menu_controller.run()

    def run(self):
        game = Game(view_cst.WIDTH, view_cst.HEIGHT)
        game.setup()
        game.initialize_character()
        game.initialize_ui()


if __name__ == "__main__":
    game = Game(view_cst.WIDTH, view_cst.HEIGHT)
    game.run()
