import pygame
from view.main_menu_view import MainMenuView
from controller.main_menu_controller import MainMenuController
from model.game_data import GameData
from model.character import Character
from model.npc import NPC
from model.item import Item
from model.quest.quest import Quest
from model.settings import Settings
from view import view_constants as view_cst
from model.map.world_map import WorldMap
from model.quest.quest_builder import QuestBuilder
from database.db_retriever import retrieve_characters, retrieve_npcs, retrieve_items, retrieve_quests, retrieve_objectives
from model.scenario.scenario import Scenario

class Game:
    def __init__(self, screen_width, screen_height):
        self.screen = None  # Initialize screen later in setup
        self.game_data = GameData() #Initializes GameData and WorldMap. Builds World Map
        self.scenario = Scenario("default", self.game_data)
        self.settings = Settings(screen_width, screen_height)

    #TODO: Build default scenario
    #TODO: Test one Objective of each type
    #TODO: Test a quest with multiple objective
    #TODO: Work on dialogue

    def initialize_scenario(self):
        self.scenario.build_scenario()

    def initialize_screen(self):
        pygame.init()
        screen = pygame.display.set_mode((view_cst.WIDTH, view_cst.HEIGHT))
        self.screen = screen

    def initialize_ui(self):
        main_menu_view = MainMenuView(self.screen)
        main_menu_controller = MainMenuController(self.game_data, main_menu_view)
        main_menu_controller.run()

    def setup(self):
        self.initialize_scenario()
        self.initialize_screen()

    def launch(self):
        self.initialize_ui()

    def run(self):
        game.setup()
        game.launch()


if __name__ == "__main__":
    game = Game(view_cst.WIDTH, view_cst.HEIGHT)
    game.run()
