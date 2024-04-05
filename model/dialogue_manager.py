
''' This class is responsible for only outputting the right dialogue to feed to the DialogueBox/Controller'''
class DialogueManager:
    def __init__(self, npc, character):
        self.npc = npc
        self.character = character


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

