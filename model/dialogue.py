class Dialogue:

    '''A dialogue is a list of text
    It has a type: chat or quest
    '''

    def __init__(self, text):
        self.text = []
        for text_chunk in text:
            self.text.append(text_chunk)
        self.dialogue_length = self.get_dialogue_length()
        self.current_text_index = 0

    def point_to_next_text(self):
        if self.current_text_index < self.dialogue_length - 1:
            self.current_text_index = self.current_text_index + 1

    def point_to_previous_text(self):
        if self.current_text_index > 0:
            self.current_text_index = self.current_text_index - 1

    def get_current_dialogue(self):
        return self.text[self.current_text_index]

    def get_dialogue_length(self):
        return len(self.text)


class QuestDialogue:
    '''A dialogue is a list of text
    It has a type: chat or quest
    '''

    def __init__(self):
        self.dialogue = {}

    def add_initialization_dialogue(self, dialogue):
        self.dialogue["initialization"] = dialogue

    def add_waiting_dialogue(self, dialogue):
        self.dialogue["waiting"] = dialogue

    def add_completion_dialogue(self, dialogue):
        self.dialogue["completion"] = dialogue

    def get_initialization_dialogue(self):
        return self.dialogue["initialization"]

    def get_waiting_dialogue(self):
        return self.dialogue["waiting"]

    def get_completion_dialogue(self):
        return self.dialogue["completion"]

