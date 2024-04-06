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
        elif self.name == "complex_quest":
            self.build_complex_quest_scenario()
        elif self.name == "ordered_quest":
            self.build_ordered_quest_scenario()
        elif self.name == "multiple_quests":
            self.build_multiple_quests_scenario()
        elif self.name == "dialogue_test":
            self.build_dialogue_test_scenario()
        elif self.name == "quest_dialogue_test":
            self.build_quest_dialogue_test_scenario()
        elif self.name == "test":
            self.build_test_scenario()

    #TODO: In the future, a scenario could be built from a file.
    def build_default_scenario(self):
        self.initialize_entities()
        self.initialize_default_inventory()
        self.initialize_items_in_world()
        self.initialize_default_quests()
        pass

    def build_complex_quest_scenario(self):
        self.initialize_entities()
        self.initialize_default_inventory()
        self.initialize_items_in_world()
        self.initialize_complex_quest()
        pass

    def build_ordered_quest_scenario(self):
        self.initialize_entities()
        self.initialize_default_inventory()
        self.initialize_items_in_world()
        self.initialize_ordered_quest()
        pass

    def build_multiple_quests_scenario(self):
        self.initialize_entities()
        self.initialize_default_inventory()
        self.initialize_items_in_world()
        self.initialize_simple_quest()
        self.initialize_complex_quest()
        self.initialize_ordered_quest()
        pass

    def build_dialogue_test_scenario(self):
        self.initialize_entities()
        self.initialize_default_inventory()
        self.initialize_items_in_world()
        self.initialize_dialogue()
        pass

    def build_quest_dialogue_test_scenario(self):
        self.initialize_entities()
        self.initialize_default_inventory()
        self.initialize_items_in_world()
        self.initialize_dialogue()
        self.initialize_quest_with_dialogue()
        pass

    def build_test_scenario(self):
        self.initialize_entities()
        pass

    #TODO: For now, inventory is determined by the position of the items in the DB. In the future it could be determined by the scenario
    def initialize_default_inventory(self):
        for item in self.game_data.items:
            if item.global_position == self.game_data.character.global_position:
                self.game_data.character.add_item_to_inventory(item)

    def initialize_items_in_world(self):
        for item in self.game_data.items:
            if item not in self.game_data.character.inventory:
                item.set_in_world(True) #Items are in the world if they are not in the inventory

    def initialize_quest_with_dialogue(self):
        npc = self.game_data.find_npc_by_name("Elder")
        plant = self.game_data.find_npc_by_name("Plant")
        quest_name = f"Kill the Plant"
        quest_description = f"Locate and kill the Plant by left-clicking on it."
        quest = self.quest_builder.build_kill_quest(quest_name, quest_description, plant.id)
        quest_initialization_dialogue = self.quest_builder.build_dialogue(["Hey you, come here!", "I saw an annoying plant in the fields north of here.",
                                         "If you can slay the plant, I will give you a reward."])
        quest_waiting_dialogue = self.quest_builder.build_dialogue(["Come back with its leaves as a proof that the deed is done."])
        quest_completion_dialogue = self.quest_builder.build_dialogue(["Hmmm, you may have potential after all. Here is your reward."])
        quest_dialogue = self.quest_builder.create_quest_dialogue(quest_initialization_dialogue, quest_waiting_dialogue, quest_completion_dialogue)
        self.game_data.add_quest(quest)
        npc.add_quest_with_dialogue(quest, quest_dialogue)
        pass

    def initialize_ordered_quest(self):
        '''Initializing a quest with several steps'''
        npc = self.game_data.find_npc_by_name("Elder")
        goblin = self.game_data.find_npc_by_name("Goblin")
        skeleton = self.game_data.find_npc_by_name("Skeleton")
        position = (1,1)
        mushroom = self.game_data.find_item_by_name("Mushroom")
        name = f"Ordered Initiation Quest"
        description = f"Go through the initiation quest to prove your worth."
        quest = self.quest_builder.initialize_ordered_quest(name, description)
        self.quest_builder.add_talk_to_npc_objective_to_quest(
            "Talk to the Elder", "Left click on the Elder", quest, npc.id)
        # self.quest_builder.add_kill_objective_to_quest(
        #     "Kill the Goblin", "Left click on the Goblin", quest, goblin.id)
        self.quest_builder.add_kill_objective_to_quest(
            "Kill the Skeleton", "Left click on the Skeleton",quest, skeleton.id)
        # self.quest_builder.add_retrieval_objective_to_quest(
        #     "Retrieve the Mushroom", "Locate and pick up the Mushroom", quest, mushroom.id)
        self.quest_builder.add_location_objective_to_quest(
            "Visit the position (1,1)", "Use the coordinates in the top left, and reach position (1,1) on the map", quest, position)
        self.game_data.add_quest(quest)
        self.game_data.character.add_quest(quest)

    def initialize_complex_quest(self):
        '''Initializing a quest with several steps'''
        npc = self.game_data.find_npc_by_name("Elder")
        goblin = self.game_data.find_npc_by_name("Goblin")
        skeleton = self.game_data.find_npc_by_name("Skeleton")
        position = (1,1)
        mushroom = self.game_data.find_item_by_name("Mushroom")
        name = f"Unordered Initiation Quest"
        description = f"Talk to the Elder to start your journey."
        quest = self.quest_builder.initialize_unordered_quest(name, description)
        self.quest_builder.add_talk_to_npc_objective_to_quest(
            "Talk to the Elder", "Left click on the Elder", quest, npc.id)
        # self.quest_builder.add_kill_objective_to_quest(
        #     "Kill the Goblin", "Left click on the Goblin", quest, goblin.id)
        self.quest_builder.add_kill_objective_to_quest(
            "Kill the Skeleton", "Left click on the Skeleton",quest, skeleton.id)
        self.quest_builder.add_retrieval_objective_to_quest(
            "Retrieve the Mushroom", "Locate and pick up the Mushroom", quest, mushroom.id)
        self.quest_builder.add_location_objective_to_quest(
            "Visit the position (1,1)", "Use the coordinates in the top left, and reach position (1,1) on the map", quest, position)
        self.game_data.add_quest(quest)
        self.game_data.character.add_quest(quest)

    def initialize_simple_quest(self):
        '''Initializing a simple quest'''
        goblin = self.game_data.find_npc_by_name("Goblin")
        name = f"Kill the Goblin"
        description = f"Locate and kill the Goblin by left-clicking on it."
        quest = self.quest_builder.build_kill_quest(name, description, goblin.id)
        self.game_data.add_quest(quest)
        self.game_data.character.add_quest(quest)

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

    def initialize_dialogue(self):
        # dialogue = ["Hello, young adventurer. This is my first dialogue.", "This is my second dialogue.", "This is my third dialogue."]
        dialogue_text_1 = ["Hey guys!", "Oh, Big Gulps, huh?", "Aaalright!", "Welp, see ya later!"]
        dialogue_text_2 = ["My name is Maximus Decimus Meridius, commander of the Armies of the North, General of the Felix Legions, Loyal servant to the true emperor, Marcus Aurelius.", "Father to a murdered son, husband to a murdered wife. And I will have my vengeance, in this life or the next."]
        dialogue_text_3 = ["Are you not entertained?"]
        dialogue_text_4 = ["Strength and honor."]

        dialogue_1 = self.quest_builder.build_dialogue(dialogue_text_1)
        dialogue_2 = self.quest_builder.build_dialogue(dialogue_text_2)
        dialogue_3 = self.quest_builder.build_dialogue(dialogue_text_3)
        dialogue_4 = self.quest_builder.build_dialogue(dialogue_text_4)


        self.game_data.find_npc_by_name("Elder").add_dialogue(dialogue_1)
        self.game_data.find_npc_by_name("Elder").add_dialogue(dialogue_2)
        self.game_data.find_npc_by_name("Elder").add_dialogue(dialogue_3)
        self.game_data.find_npc_by_name("Elder").add_dialogue(dialogue_4)

        # self.game_data.find_npc_by_name("Elder").add_dialogue("Hello, young adventurer. This is my first dialogue.")
        # self.game_data.find_npc_by_name("Elder").add_dialogue("This is my second dialogue.")
        # self.game_data.find_npc_by_name("Elder").add_dialogue("This is my third dialogue.")


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