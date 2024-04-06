import model.quest.objective

class QuestManager():
    def __init__(self, game_data):
        self.game_data = game_data

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