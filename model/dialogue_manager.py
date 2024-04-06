import random
import model.model_constants as model_cst


''' This class is responsible for only outputting the right dialogue to feed to the DialogueBox/Controller'''
class DialogueManager:
    def __init__(self, npc, character):
        self.npc = npc
        self.character = character

    def get_dialogue(self):
        if self.check_npc_has_quests():
            print("NPC has quests, picking a quest at random")
            quest = self.get_random_npc_quest()
            quest_id = quest.get_id()
            print(f"Quest name is: {quest.name}")
            quest_dialogue = self.npc.quests_dialogue[quest.get_id()]
            print(f"Quest dialogue is: {quest_dialogue}")
            #TODO: Check if the character already has the quest
            if self.character.check_character_has_quest(quest_id):
                print("Character already has the quest")
                #TODO: Check if the quest is already active or completed
                if quest.completed:
                    print("Quest is completed")
                    dialogue = quest_dialogue.get_completion_dialogue()
                    return dialogue, "quest"
                else:
                    print("Quest is not completed")
                    dialogue = quest_dialogue.get_waiting_dialogue()
                    return dialogue, "quest"
            else:
                print("Character does not have the quest")
                dialogue = quest_dialogue.get_initialization_dialogue()
                return dialogue, "quest"
        else:
            print("NPC has no quests, getting dialogue")
            if self.check_npc_has_dialogue():
                print("NPC has dialogue, getting random dialogue")
                return self.get_random_npc_dialogue(), "chat"
            else:
                print("NPC has no dialogue, getting generic dialogue")
                return self.get_random_generic_dialogue(), "chat"
                pass

    def check_npc_has_quests(self):
        if len(self.npc.quests) > 0:
            return True
        else:
            return False

    def check_npc_has_dialogue(self):
        if len(self.npc.dialogue) > 0:
            return True
        else:
            return False

    def get_random_generic_dialogue(self):
        random_index = random.randint(0, len(model_cst.GENERIC_DIALOGUES) - 1)
        return model_cst.GENERIC_DIALOGUES[random_index]

    def get_random_npc_dialogue(self):
        random_index = random.randint(0, len(self.npc.dialogue) - 1)
        print(f"Length of NPC dialogue is {len(self.npc.dialogue)}")
        print(f"Random index is {random_index}")
        return self.npc.dialogue[random_index]

    #TODO: Move this logic somewhere else
    def get_random_npc_quest(self):
        random_index = random.randint(0, len(self.npc.quests) - 1)
        return self.npc.quests[random_index]