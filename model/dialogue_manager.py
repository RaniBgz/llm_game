import random
import model.model_constants as model_cst


''' This class is responsible for only outputting the right dialogue to feed to the DialogueBox/Controller'''
class DialogueManager:
    def __init__(self, npc, character):
        self.npc = npc
        self.character = character

    def get_dialogue(self):
        if self.check_npc_has_quests():
            print("NPC has quests")
        else:
            print("NPC has no quests, getting dialogue")
            if self.check_npc_has_dialogue():
                print("NPC has dialogue, getting random dialogue")
                return self.get_random_npc_dialogue()
            else:
                print("NPC has no dialogue, getting generic dialogue")
                return self.get_random_generic_dialogue()
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