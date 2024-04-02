''' Defines the scenario of the game. Builds the quests, associates them to the right targets, and associates them to a NPC'''

from database.db_retriever import retrieve_characters, retrieve_npcs, retrieve_items
from model.game_data import GameData
from model.quest.quest_builder import QuestBuilder

class Scenario:
    def __init__(self, name, game_data):
        self.name = name
        self.game_data = game_data
        self.quest_builder = QuestBuilder()

    def build_scenario(self):
        if self.name == "default":
            self.build_default_scenario()
        elif self.name == "test":
            self.build_test_scenario()

    #TODO: In the future, a scenario could be built from a file.
    def build_default_scenario(self):
        self.initialize_entities()
        self.initialize_default_inventory()
        self.initialize_default_quests()
        pass

    def build_test_scenario(self):
        self.initialize_entities()
        pass

    #TODO: For now, inventory is determined by the position of the items in the DB. In the future it could be determined by the scenario
    def initialize_default_inventory(self):
        for item in self.game_data.items:
            if item.global_position == self.game_data.character.global_position:
                self.game_data.character.add_item_to_inventory(item)

    #TODO: Handle creation of multi-objective quests
    def initialize_default_quests(self):
        for npc in self.game_data.npcs:
            # Building Kill Quests
            if npc.hostile:
                name = f"Kill the {npc.name}"
                description = f"Find and Kill the {npc.name} by left-clicking on it."
                quest = self.quest_builder.build_kill_quest(name, description, npc.id)
                self.game_data.add_quest(quest) #Ading the quest in the general list of quests in the game
                self.game_data.character.add_quest(quest) #Specifically assigning the quest to the character
            # Building Talk to NPC Quests
            elif not npc.hostile:
                name = f"Talk to the {npc.name}"
                description = f"Find and Talk to the {npc.name} by left-clicking on it."
                quest = self.quest_builder.build_talk_to_npc_quest(name, description, npc.id)
                self.game_data.add_quest(quest)
                self.game_data.character.add_quest(quest)

        #Building Retrieval Quests
        for item in self.game_data.items:
            if item not in self.game_data.character.inventory:
                name = f"Retrieve the {item.name}"
                description = f"Find and Retrieve the {item.name} by left-clicking on it."
                quest = self.quest_builder.build_retrieval_quest(name, description, item.id)
                self.game_data.add_quest(quest)
                self.game_data.character.add_quest(quest)

        #Building Location Quest
        name = f"Go to position (4, 4)"
        description = f"Explore the map and find the position (4, 4)."
        quest = self.quest_builder.build_location_quest(name, description, (4, 4))
        self.game_data.add_quest(quest)
        self.game_data.character.add_quest(quest)


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

        # self.initialize_quests()

    # def initialize_quests(self):
    #     quests = retrieve_quests()
    #     for quest in quests:
    #         if quest.name == "Kill the Plant":
    #             quest.active = True
    #             npc = self.game_data.find_npc_by_name("Plant")
    #             quest = self.game_data.quest_builder.add_kill_objective_to_quest(quest, npc.id)
    #             print(f"Quest created for npc {npc.id} with name {npc.name}")
    #             self.game_data.character.add_quest(quest)
    #         elif quest.name == "Talk to the Elder":
    #             quest.active = True
    #             npc = self.game_data.find_npc_by_name("Elder")
    #             quest = self.game_data.quest_builder.add_talk_to_npc_objective_to_quest(quest, npc.id)
    #             self.game_data.character.add_quest(quest)
    #             pass
    #         # elif quest.name == "Retrieve the Steak":
    #         #     quest.active = True
    #         #     item = self.model.find_item_by_name("Steak")
    #         #     quest = self.model.quest_builder.add_retrieval_objective_to_quest(quest, item.id)
    #         #     self.model.character.add_quest(quest)
    #         else:
    #             quest.active = False


if __name__ == '__main__':
    game_data = GameData()
    scenario = Scenario("default", game_data)
    scenario.build_scenario()