class Dialogue:

    '''A dialogue is a list of text
    It has a type: chat or quest
    '''

    def __init__(self, text, dialogue_type):
        self.text = []
        for text_chunk in text:
            self.text.append(text_chunk)
        self.dialogue_type = dialogue_type
        self.current_text_index = 0

    def point_to_next_text(self):
        self.current_text_index += 1

    def point_to_previous_text(self):
        self.current_text_index -= 1

    def get_current_dialogue(self):
        return self.text[self.current_text_index]

