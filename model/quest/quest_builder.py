from model.quest.quest import Quest
from model.quest.objective import KillObjective

'''Links quests to objectives'''

class QuestBuilder():
    def __init__(self):
        pass

    def build_kill_quest(self, quest, target_id):
        kill_objective = KillObjective(target_id)
        quest.objectives.append(kill_objective)
        return quest
