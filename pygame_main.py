import pygame
from view.main_menu_view import MainMenuView
from controller.main_menu_controller import MainMenuController
from controller.game_controller import GameController
from model.game_data import GameData
from model.settings import Settings
from view import view_constants as view_cst
from model.scenario.scenario import Scenario

class Game:
    def __init__(self, screen_width, screen_height):
        self.screen = None  # Initialize screen later in setup
        # print(f"Before game data init")
        self.game_data = GameData() #Initializes GameData and WorldMap. Builds World Map
        # print(f"After game data init")
        # self.scenario = Scenario("default", self.game_data)
        # self.scenario = Scenario("complex_quest", self.game_data)
        # self.scenario = Scenario("ordered_quest", self.game_data)
        self.scenario = Scenario("quest_dialogue_test", self.game_data)
        self.settings = Settings(screen_width, screen_height)
        self.game_controller = None

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

    def initialize_game_controller(self):
        # Initialize the GameController with necessary dependencies
        self.game_controller = GameController(self.screen, self.game_data)
        # Let GameController handle the state management and UI initialization
        self.game_controller.run()

    def initialize_ui(self):
        main_menu_view = MainMenuView(self.screen)
        main_menu_controller = MainMenuController(self.game_data, main_menu_view)
        main_menu_controller.run()

    def setup(self):
        self.initialize_scenario()
        self.initialize_screen()
        self.initialize_game_controller()

    # def launch(self):
    #     self.initialize_ui()

    def run(self):
        game.setup()
        # game.launch()


if __name__ == "__main__":
    game = Game(view_cst.WIDTH, view_cst.HEIGHT)
    game.run()
