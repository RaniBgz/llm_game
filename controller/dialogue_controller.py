import pygame

class DialogueController:
    def __init__(self, screen, dialogue_box, npc, character):
        self.character = character
        self.screen = screen
        self.dialogue_box = dialogue_box
        self.npc = npc
        self.dialogues = npc.dialogue
        self.current_dialogue_index = 0
        self.total_dialogues = len(self.dialogues)

    def start_dialogue(self):
        dialogue_text = self.dialogues[self.current_dialogue_index]
        self.dialogue_box.create_dialogue(self.npc, dialogue_text, self.current_dialogue_index, self.total_dialogues)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.dialogue_box.close_button_rect and self.dialogue_box.close_button_rect.collidepoint(event.pos):
                self.dialogue_box.show = False
            elif self.dialogue_box.prev_button_rect and self.dialogue_box.prev_button_rect.collidepoint(event.pos):
                self.current_dialogue_index = max(self.current_dialogue_index - 1, 0)
                self.start_dialogue()
            elif self.dialogue_box.next_button_rect and self.dialogue_box.next_button_rect.collidepoint(event.pos):
                self.current_dialogue_index = min(self.current_dialogue_index + 1, self.total_dialogues - 1)
                self.start_dialogue()