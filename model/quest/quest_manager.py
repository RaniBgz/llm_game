import model.quest.objective
import random

class QuestManager():
    def __init__(self, game_data):
        self.game_data = game_data
        self.current_npc = None
        #TODO: For now, only one current quest is handled per NPC
        self.current_quests = self._build_initial_quest_data()

    def set_current_npc(self, npc):
        self.current_npc = npc

    def _build_initial_quest_data(self):
        current_quests = {}
        for npc in self.game_data.npcs:
            if npc not in current_quests:
                current_quests[npc] = []
            next_quest = self._get_next_available_quest(npc)
            if next_quest:
                current_quests[npc].append(next_quest)
                # current_quests[npc] = [next_quest]
        return current_quests

    def _get_next_available_quest(self, npc):
        for quest in npc.quests:
            if not quest.ended:
                return quest
        return None

    def get_next_npc_quest(self, npc):
        if len(npc.quests) == 0:
            return None
        else:
            #TODO: if npc doesn't start with a quest, might be an issue later
            for i in range(len(npc.quests)):
                if not npc.quests[i].ended:
                    self.current_quests[npc].append(npc.quests[i])
                    return npc.quests[i]
            return None

    def initialize_next_npc_quest(self, npc):
        next_quest = self._get_next_available_quest(npc)
        if next_quest:
            self.current_quests[npc] = [next_quest]

    def add_quest_with_dialogue_to_current_npc(self, quest, quest_dialogue):
        self.current_npc.add_quest_with_dialogue(quest, quest_dialogue)

    def handle_quest_giving(self):
        if self.current_npc and self.current_quests.get(self.current_npc):
            quest = self.current_quests[self.current_npc].pop(0)  # Remove and hand out
            self.game_data.character.add_quest(quest)
            # quest.set_started()  # Or adjust the status accordingly

#TODO: for retrieval sub objectives remove the item from the player's inventory
    def handle_quest_completion(self):
        quest = self.current_quests.get(self.current_npc, [])[0]
        quest.set_ended()
        self.handle_quest_objective_completion(quest)
        self.game_data.character.remove_quest(quest)


    def handle_quest_objective_completion(self, quest):
        for objective in quest.get_objectives():
            #Take the item away from the player's inventory for retrieval quests
            if isinstance(objective, model.quest.objective.RetrievalObjective):
                item = self.game_data.find_item_by_id(objective.target_item_id)
                if self.game_data.character.has_item(objective.target_item_id):
                    self.game_data.character.remove_item_from_inventory(item)


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