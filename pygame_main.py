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
from database.db_retriever import retrieve_characters, retrieve_npcs, retrieve_items, retrieve_quests, retrieve_objectives


class Game:
    def __init__(self, screen_width, screen_height):
        self.screen = None  # Initialize screen later in setup
        self.model = GameData()
        self.settings = Settings(screen_width, screen_height)

    def initialize_world(self):
        self.model.world_map = WorldMap.get_instance()
        self.model.world_map.build_map(20, 20)
        self.model.world_map.set_player_coords(0, 0)

    #TODO: load npcs, items and quests from database and make sure everything works correctly
    #TODO: add entities_dict back to local map and start linking view with entities
    #TODO: Handle interactions for friendly npcs
    #TODO: Handle interactions for hostile npcs
    #TODO: Inspect with right click (display stats)
    #TODO: Dialogue logic with NPCs
    #
    # def initialize_npcs(self):
    #     elder = NPC("Lieutenant Goblin", 8)
    #     self.model.world_map.add_npc_to_map(1, 2, goblin_monster)


    def initialize_quests(self):
        quests = retrieve_quests()
        for quest in quests:
            self.model.character.add_quest(quest)
        # pass
        # self.model.quest_builder = QuestBuilder()
        # #Creating goblin and positioning it on the world map
        # goblin_monster = NPC("Elder", 8, sprite="./assets/sprites/npcs/elder.png", global_position=(0, 0), local_position=(4, 3))
        # print(f"NPC: {goblin_monster.name} at {goblin_monster.local_position}")
        # self.model.world_map.add_entity(goblin_monster, (0, 0))
        #
        # #Defining a kill goblin quest and adding it to the character
        # kill_goblin_quest = self.model.quest_builder.create_kill_quest(goblin_monster.name, goblin_monster.id)
        # self.model.character.add_quest(kill_goblin_quest)
        #
        # #Creating generic quests and adding them to the character
        # self.model.character.add_quest(Quest("Defeat the Mage", "Find and defeat the Mage King", True))
        # self.model.character.add_quest(Quest("Find the Hidden Treasure", "Follow the clues...", False))

    def initialize_character(self):
        characters = retrieve_characters()
        self.model.character = characters[0]
        # self.model.character = Character("Player", 16, global_position=(0, 0), local_position=(view_cst.H_TILES//2, 3*view_cst.V_TILES//4))
        print(f"Character: {self.model.character.name} at {self.model.character.local_position}")
        # self.model.character.current_map = self.model.world_map.get_local_map_at(0, 0)
        self.model.world_map.add_entity(self.model.character, self.model.character.global_position)

    def initialize_npcs(self):
        npcs = retrieve_npcs()
        for npc in npcs:
            self.model.world_map.add_entity(npc, npc.global_position)

    def initialize_items(self):
        items = retrieve_items()
        for item in items:
            self.model.character.add_item_to_inventory(item)

    def initialize_inventory(self):
        self.model.character.add_item_to_inventory(Item("Sword", "A Rusty Sword"))
        self.model.character.add_item_to_inventory(Item("Healing Potion", "Restores Health"))

    def setup(self):
        self.initialize_world()
        self.initialize_character()
        self.initialize_npcs()
        self.initialize_items()
        # self.initialize_inventory()
        self.initialize_quests()
        self.initialize_screen()

    def initialize_screen(self):
        pygame.init()
        screen = pygame.display.set_mode((view_cst.WIDTH, view_cst.HEIGHT))
        self.screen = screen

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



    #TODO: Separate world initialization from the rest

    # def setup_world(world_map):
    #     # Create local maps and add them to the world map
    #     # ...
    #
    #     # Create NPCs
    #     goblin_monster = NPC("Lieutenant Goblin", 8)
    #     world_map.add_entity(goblin_monster, (1, 2))  # Place goblin at local map (1, 2)
    #

