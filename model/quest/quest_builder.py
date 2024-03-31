from model.quest.quest import Quest
from model.quest.objective import KillObjective

class QuestBuilder():
    def __init__(self):
        pass

    def create_kill_quest(self, target_name, target_id, active=False):
        kill_quest = Quest("Defeat the " + target_name, f"Find and defeat the {target_name}.", active)
        kill_objective = KillObjective(target_id)
        kill_quest.objective = kill_objective
        return kill_quest
