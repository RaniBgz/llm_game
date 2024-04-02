''' Defines the scenario of the game. Builds the quests, associates them to the right targets, and associates them to a NPC'''

from database.db_retriever import retrieve_characters, retrieve_npcs, retrieve_items
from model.game_data import GameData

class Scenario:
    def __init__(self, name, game_data):
        self.name = name
        self.game_data = game_data

    def build_scenario(self):
        if self.name == "default":
            self.build_default_scenario()
        elif self.name == "test":
            self.build_test_scenario()

    def build_default_scenario(self):
        self.initialize_entities()
        pass

    def build_quests(self, quest_builder):
        pass


    def initialize_entities(self):
        self.game_data.set_character(retrieve_characters()[0])
        print(f"Character: {self.game_data.character}")
        npcs = retrieve_npcs()
        print(f"NPCs: {npcs}")
        items = retrieve_items()
        print(f"Items: {items}")
        for npc in npcs:
            self.game_data.add_npc(npc)
        for item in items:
            self.game_data.add_item(item)


if __name__ == '__main__':
    game_data = GameData()
    scenario = Scenario("default", game_data)
    scenario.build_scenario()