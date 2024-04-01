from model.quest.quest import Quest
from model.quest.objective import KillObjective, LocationObjective, RetrievalObjective, TalkToNPCObjective

'''Links quests to objectives'''

class QuestBuilder():
    def __init__(self):
        pass

    def add_kill_objective_to_quest(self, quest, target_id):
        kill_objective = KillObjective(target_id)
        quest.objectives.append(kill_objective)
        return quest

    def add_talk_to_npc_objective_to_quest(self, quest, target_npc_id):
        talk_to_npc_objective = TalkToNPCObjective(target_npc_id)
        quest.objectives.append(talk_to_npc_objective)
        return quest

    def add_location_objective_to_quest(self, quest, target_location):
        location_objective = LocationObjective(target_location)
        quest.objectives.append(location_objective)
        return quest
