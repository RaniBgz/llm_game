import pygame
from view.main_menu_view import MainMenuView
from controller.main_menu_controller import MainMenuController
from model.game_data import GameData
from model.character import Character
from model.npc import NPC
from model.item import Item
from model.quests.quest import Quest
from model.settings import Settings
from view import view_constants as view_cst
from model.maps.world_map import WorldMap
from model.quests.quest_builder import QuestBuilder

#TODO: find a place to store that

class Game:
    def __init__(self, screen_width, screen_height):
        self.screen = None  # Initialize screen later in setup
        self.model = GameData()
        self.settings = Settings(screen_width, screen_height)

    #TODO: Separate world initialization from the rest

    # def setup_world(world_map):
    #     # Create local maps and add them to the world map
    #     # ...
    #
    #     # Create NPCs
    #     goblin_monster = NPC("Lieutenant Goblin", 8)
    #     world_map.add_entity(goblin_monster, (1, 2))  # Place goblin at local map (1, 2)
    #

    def setup(self):
        world_map = WorldMap.get_instance()
        world_map.build_map(10, 10)
        world_map.set_player_coords(0, 0)
        self.model.quest_builder = QuestBuilder()
        self.initialize_character()
        self.model.character.current_map = world_map
        # Set up initial map location (assuming you have map setup logic)
        # initial_x, initial_y = 0, 0  # Replace with your desired start coordinates
        # initial_map = world_map.get_local_map_at(initial_x, initial_y)
        # self.model.character.change_map(initial_map)
        self.screen = self.initialize_screen()

    # def on_npc_death(self, npc):
    #     for quest in self.model.character.quests:
    #         if isinstance(quest.objective, KillObjective) and quest.objective.target_id == npc.id:
    #     # Mark quest as completed or perform other quest completion logic and rewards!

    def initialize_character(self):
        self.model.character = Character(16)
        self.model.character.add_item_to_inventory(Item("Sword", "A Rusty Sword"))
        self.model.character.add_item_to_inventory(Item("Healing Potion", "Restores Health"))
        self.model.character.add_quest(Quest("Defeat the Goblin", "Find and defeat the Goblin King", True))
        self.model.character.add_quest(Quest("Find the Hidden Treasure", "Follow the clues...", False))

        goblin_monster = NPC("Lieutenant Goblin", 8)
        kill_goblin_quest = self.model.quest_builder.create_kill_quest(goblin_monster.name, goblin_monster.id)
        self.model.character.add_quest(kill_goblin_quest)

        # goblin_id = self.model.npc_list[0].id
        # print(f"Goblin id: {self.model.npc_list[0].id}")
        # created_goblin = self.model.find_npc_by_id(goblin_id)
        # print(f"Created Goblin id: {created_goblin.id}")
        # self.model.quest_builder().create_kill_quest("Goblin", 8)

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
        game.initialize_ui()


if __name__ == "__main__":
    game = Game(view_cst.WIDTH, view_cst.HEIGHT)
    game.run()
