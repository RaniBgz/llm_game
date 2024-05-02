import random
import model.model_constants as model_cst


''' This class is responsible for only outputting the right dialogue to feed to the DialogueBox/Controller'''
class DialogueManager:
    def __init__(self, npc, character, quest):
        self.npc = npc
        self.character = character
        self.quest = quest

    def get_dialogue(self):
        if self.quest is not None:
            quest_id = self.quest.get_id()
            quest_dialogue = self.npc.get_quest_dialogue(quest_id)
            if self.character.check_character_has_quest(quest_id):
                if self.quest.completed:
                    dialogue = quest_dialogue.get_completion_dialogue()
                    return dialogue, "quest_completion"
                else:
                    dialogue = quest_dialogue.get_waiting_dialogue()
                    return dialogue, "quest_waiting"
            else:
                dialogue = quest_dialogue.get_initialization_dialogue()
                return dialogue, "quest_initialization"
        else:
            if self.check_npc_has_dialogue():
                return self.get_random_npc_dialogue(), "chat"
            else:
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
