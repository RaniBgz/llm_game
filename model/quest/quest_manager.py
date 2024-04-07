import model.quest.objective
import random

class QuestManager():
    def __init__(self, game_data):
        self.game_data = game_data
        self.current_quests = {}
        self.current_npc = None
        self.initialize_current_quests()

    def set_current_npc(self, npc):
        self.current_npc = npc

    ''' Quest initialization and attribution methods'''
    def give_quest_to_character(self):
        print(f"Giving quest to character")
        quest = self.current_quests[self.current_npc][0]
        self.game_data.character.add_quest(quest)
        print(f"Quest {quest.id} given to character")

    #FLAW IN THE LOGIC: if several NPCs give out quests, we'll have problems (may be fixed)
    #FLAW IN THE LOGIC: does that give quests on a loop?
    def remove_quest_from_character(self):
        quest = self.current_quests[self.current_npc][0]
        quest.set_ended()
        self.current_quests[self.current_npc].remove(quest)
        self.game_data.character.remove_quest(quest)
        print(f"Quest {quest.id} removed from character")

    def get_next_npc_quest(self, npc):
        if len(npc.quests) == 0:
            return None
        else:
            for i in range(len(npc.quests)):
                if not npc.quests[i].ended:
                    self.current_quests[npc].append(npc.quests[i])
                return npc.quests[i]
            return None

    #Okay, this is cool, but NPC need to have quest associated to them (some other logic)
    #AKA quests in game data are not affected by this
    def initialize_current_quests(self):
        for npc in self.game_data.npcs:
            if len(npc.quests) > 0:
                self.current_quests[npc] = []

    ''' Quest completion methods '''
    def check_location_objective_completion(self):
        for quest in self.game_data.character.quests:
            if quest.ordered:
                current_objective = quest.get_current_objective()
                if isinstance(current_objective, model.quest.objective.LocationObjective):
                    if current_objective.target_location == self.game_data.character.global_position:
                        current_objective.set_completed()
                        print(f"Objective {current_objective.id} for quest {quest.id} is now complete")
                        if not quest.point_to_next_objective():
                            quest.set_inactive()
                            print(f"Quest {quest.id} is now complete")
            else:
                for objective in quest.objectives:
                    if isinstance(objective, model.quest.objective.LocationObjective):
                        if objective.target_location == self.game_data.character.global_position:
                            objective.set_completed()
                            print(f"Objective {objective.id} for quest {quest.id} is now complete")
                            if quest.check_all_objectives_completed():
                                quest.set_inactive()
                                print(f"Quest {quest.id} is now complete")


    def check_kill_objective_completion(self, npc):
        for quest in self.game_data.character.quests:
            print(f"Checking quest {quest.id}")
            if quest.ordered:
                current_objective = quest.get_current_objective()
                if isinstance(current_objective, model.quest.objective.KillObjective):
                    if current_objective.target_id == npc.id:
                        current_objective.set_completed()
                        print(f"Objective {current_objective.id} for quest {quest.id} is now complete")
                        if not quest.point_to_next_objective():
                            quest.set_inactive()
                            print(f"Quest {quest.id} is now complete")
            else:
                for objective in quest.objectives:
                    if isinstance(objective, model.quest.objective.KillObjective):
                        if objective.target_id == npc.id:
                            objective.set_completed()
                            print(f"Objective {objective.id} for quest {quest.id} is now complete")
                            if quest.check_all_objectives_completed():
                                quest.set_inactive()
                                print(f"Quest {quest.id} is now complete")


    def check_talk_to_npc_objective_completion(self, npc):
        for quest in self.game_data.character.quests:
            if quest.ordered:
                current_objective = quest.get_current_objective()
                if isinstance(current_objective, model.quest.objective.TalkToNPCObjective):
                    if current_objective.target_npc_id == npc.id:
                        current_objective.set_completed()
                        print(f"Objective {current_objective.id} for quest {quest.id} is now complete")
                        if not quest.point_to_next_objective():
                            quest.set_inactive()
                            print(f"Quest {quest.id} is now complete")
            else:
                for objective in quest.objectives:
                    if isinstance(objective, model.quest.objective.TalkToNPCObjective):
                        if objective.target_npc_id == npc.id:
                            objective.set_completed()
                            print(f"Objective {objective.id} for quest {quest.id} is now complete")
                            if quest.check_all_objectives_completed():
                                quest.set_inactive()
                                print(f"Quest {quest.id} is now complete")

    def check_retrieval_objective_completion(self, item):
        for quest in self.game_data.character.quests:
            if quest.ordered:
                current_objective = quest.get_current_objective()
                if isinstance(current_objective, model.quest.objective.RetrievalObjective):
                    if current_objective.target_item_id == item.id:
                        current_objective.set_completed()
                        print(f"Objective {current_objective.id} for quest {quest.id} is now complete")
                        if not quest.point_to_next_objective():
                            quest.set_inactive()
                            print(f"Quest {quest.id} is now complete")
            else:
                for objective in quest.objectives:
                    if isinstance(objective, model.quest.objective.RetrievalObjective):
                        if objective.target_item_id == item.id:
                            objective.set_completed()
                            print(f"Objective {objective.id} for quest {quest.id} is now complete")
                            if quest.check_all_objectives_completed():
                                quest.set_inactive()
                                print(f"Quest {quest.id} is now complete")