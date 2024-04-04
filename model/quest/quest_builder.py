from model.quest.quest import Quest
from model.quest.objective import KillObjective, LocationObjective, RetrievalObjective, TalkToNPCObjective
from model.dialogue import Dialogue

'''Links quests to objectives'''

class QuestBuilder():
    def __init__(self):
        pass

    '''Write "initialize x quest" methods here for complex quests with objectives that have their own descriptions and names.'''
    def initialize_ordered_quest(self, name, description):
        quest = Quest(name, description, ordered=True)
        return quest

    def initialize_unordered_quest(self, name, description):
        quest = Quest(name, description)
        return quest

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

    def build_dialogue(self, text, dialogue_type):
        dialogue = Dialogue(text, dialogue_type)
        return dialogue
