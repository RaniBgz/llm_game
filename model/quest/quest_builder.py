from model.quest.quest import Quest
from model.quest.objective import KillObjective, LocationObjective, RetrievalObjective, TalkToNPCObjective
from model.dialogue.dialogue import Dialogue, QuestDialogue
from database.db_retriever import DBRetriever
from sentence_transformers import SentenceTransformer, util

'''Links quests to objectives'''

class QuestBuilder():
    def __init__(self, game_data):
        self.game_data = game_data
        self.db_retriever = DBRetriever()

    ''' Methods to generate quests and dialogue with llm_model and semantic_kernel'''
    async def generate_quest_and_dialogue(self, llm_model, genre="fantasy", difficulty="easy"):
        print(f"Generating quest")
        quest_json = await llm_model.generate_unit_quest(genre, difficulty)
        print(f"Generated quest json: {quest_json}")
        quest = self.create_quest_from_json(quest_json)
        print(f"Generating dialogue associated with quest")
        dialogue_json = await llm_model.generate_unit_quest_dialogue(quest_json)
        print(f"Generated dialogue json: {dialogue_json}")
        quest_dialogue = self.create_quest_dialogue_from_json(dialogue_json)
        return quest, quest_dialogue

    async def generate_quest_and_dialogue_with_context(self, llm_model, game_context, genre="fantasy", difficulty="easy"):
        print(f"Generating quest")
        quest_json = await llm_model.generate_unit_quest_with_context(game_context, genre, difficulty)
        print(f"Generated quest json: {quest_json}")
        quest = self.create_quest_from_json(quest_json)
        print(f"Generating dialogue associated with quest")
        dialogue_json = await llm_model.generate_unit_quest_dialogue(quest_json)
        print(f"Generated dialogue json: {dialogue_json}")
        quest_dialogue = self.create_quest_dialogue_from_json(dialogue_json)
        return quest, quest_dialogue

    def create_quest_from_json(self, quest_json):
        quest = Quest(
            name=quest_json["name"],
            description=quest_json["description"],
            ordered=quest_json["ordered"],
        )

        # Create the objectives
        for obj in quest_json["objectives"]:
            if obj["type"] == "kill":
                objective = KillObjective(obj["name"], obj["description"], obj["target"])
                npc = self.game_data.find_npc_by_name(obj["target"]) #Trying to find the NPC in the game data
                if npc is None:
                    most_similar_npc = self.game_data.find_most_similar_npc(obj["target"]) #If not found, try to find the most similar NPC
                    print("Most similar NPC: ", most_similar_npc)
            elif obj["type"] == "location":
                objective = LocationObjective(obj["name"], obj["description"], obj["target"])
            elif obj["type"] == "retrieval":
                objective = RetrievalObjective(obj["name"], obj["description"], obj["target"])
                item = self.game_data.find_item_by_name(obj["target"])
                if item is None:
                    raise ValueError(f"Item {obj['target']} not found")
            elif obj["type"] == "talk_to_npc":
                objective = TalkToNPCObjective(obj["name"], obj["description"], obj["target"])
                npc = self.game_data.find_npc_by_name(obj["target"])
                if npc is None:
                    raise ValueError(f"NPC {obj['target']} not found")
            else:
                raise ValueError(f"Invalid objective type: {obj['type']}")

            quest.objectives.append(objective)

        return quest

    def create_quest_dialogue_from_json(self, dialogue_json):
        initialization_dialogue = self.build_dialogue(dialogue_json["initialization"])
        waiting_dialogue = self.build_dialogue(dialogue_json["waiting"])
        completion_dialogue = self.build_dialogue(dialogue_json["completion"])
        quest_dialogue = QuestDialogue()
        quest_dialogue.add_initialization_dialogue(initialization_dialogue)
        quest_dialogue.add_waiting_dialogue(waiting_dialogue)
        quest_dialogue.add_completion_dialogue(completion_dialogue)
        return quest_dialogue


    '''Write "initialize x quest" methods here for complex quests with objectives that have their own descriptions and names.'''
    def initialize_ordered_quest(self, name, description):
        quest = Quest(name, description, ordered=True)
        return quest

    def initialize_unordered_quest(self, name, description):
        quest = Quest(name, description)
        return quest

    '''Quest Dialogue methods'''
    def create_quest_dialogue(self, initial_dialogue, waiting_dialogue, completion_dialogue):
        quest_dialogue = QuestDialogue()
        quest_dialogue.add_initialization_dialogue(initial_dialogue)
        quest_dialogue.add_waiting_dialogue(waiting_dialogue)
        quest_dialogue.add_completion_dialogue(completion_dialogue)
        return quest_dialogue


    '''Methods to build single-objective quests'''
    def build_kill_quest(self, name, description, target_id):
        quest = Quest(name, description)
        kill_objective = KillObjective(name, description, target_id)
        quest.add_objective(kill_objective)
        return quest

    def build_talk_to_npc_quest(self, name, description, target_npc_id):
        quest = Quest(name, description)
        talk_to_npc_objective = TalkToNPCObjective(name, description, target_npc_id)
        quest.add_objective(talk_to_npc_objective)
        return quest

    def build_retrieval_quest(self, name, description, target_item_id):
        quest = Quest(name, description)
        retrieval_objective = RetrievalObjective(name, description,target_item_id)
        quest.add_objective(retrieval_objective)
        return quest

    def build_location_quest(self, name, description, target_location):
        quest = Quest(name, description)
        location_objective = LocationObjective(name, description, target_location)
        quest.add_objective(location_objective)
        return quest

    '''Methods to add objectives to existing quests'''
    def add_kill_objective_to_quest(self, name, description, quest, target_id):
        kill_objective = KillObjective(name, description, target_id)
        quest.add_objective(kill_objective)
        return quest

    def add_talk_to_npc_objective_to_quest(self, name, description, quest, target_npc_id):
        talk_to_npc_objective = TalkToNPCObjective(name, description, target_npc_id)
        quest.add_objective(talk_to_npc_objective)
        return quest

    def add_location_objective_to_quest(self, name, description, quest, target_location):
        location_objective = LocationObjective(name, description, target_location)
        quest.add_objective(location_objective)
        return quest

    def add_retrieval_objective_to_quest(self, name, description, quest, target_item_id):
        retrieval_objective = RetrievalObjective(name, description, target_item_id)
        quest.add_objective(retrieval_objective)
        return quest

    def build_dialogue(self, text):
        dialogue = Dialogue(text)
        return dialogue
