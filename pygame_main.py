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


class Game:
    def __init__(self, screen_width, screen_height):
        self.screen = None  # Initialize screen later in setup
        self.model = GameData() #Initializes GameData and WorldMap
        self.settings = Settings(screen_width, screen_height)

    def initialize_world(self):
        self.model.world_map.build_map(20, 20)

    #TODO: Have a way to lookup quests
    #TODO: NPC retrieval by name? Handle multiple NPCs with same name? Subclass NPC?

    #TODO: Test one Objective of each type
    #TODO: Test a quest with multiple objective
    #TODO: Standardize UI elements
    #TODO: Work on dialogue

    #This will possibly become a scenario builder
    def initialize_quests(self):
        quests = retrieve_quests()
        for quest in quests:
            if quest.name == "Kill the Plant":
                quest.active = True
                npc = self.model.find_npc_by_name("Plant")
                quest = self.model.quest_builder.add_kill_objective_to_quest(quest, npc.id)
                print(f"Quest created for npc {npc.id} with name {npc.name}")
                self.model.character.add_quest(quest)
                # quest.objectives.append(QuestBuilder.build_kill_objective(1))
            elif quest.name == "Talk to the Elder":
                quest.active = True
                npc = self.model.find_npc_by_name("Elder")
                quest = self.model.quest_builder.add_talk_to_npc_objective_to_quest(quest, npc.id)
                self.model.character.add_quest(quest)
                pass
            else:
                quest.active = False


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
            self.model.world_map.add_entity(npc, npc.global_position) #Add NPC to right local map through world map
            self.model.npcs.append(npc) #Add NPC to global list of NPC for now (need better storage/retrieval strat)

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
