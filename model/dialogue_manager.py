import random

class DialogueManager:
    def __init__(self, game_data):
        self.game_data = game_data
        self.current_dialogue = None
        self.current_npc = None
        self.dialogue_history = []

    def start_dialogue(self, npc):
        self.current_npc = npc
        self.current_dialogue = random.choice(npc.dialogue)
        self.dialogue_history.append(self.current_dialogue)
        return self.current_dialogue

    def continue_dialogue(self):
        if self.current_dialogue:
            next_dialogue = self.current_dialogue.get_next_dialogue()
            if next_dialogue:
                self.current_dialogue = next_dialogue
                self.dialogue_history.append(next_dialogue)
                return next_dialogue
        return None

    def end_dialogue(self):
        self.current_npc = None
        self.current_dialogue = None

    def handle_quest(self, quest_id):
        # Handle quest logic here
        pass