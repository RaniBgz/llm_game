import pygame
import random

class DialogueController:
    def __init__(self, screen, dialogue_box, npc, character):
        self.character = character
        self.screen = screen
        self.dialogue_box = dialogue_box
        self.npc = npc
        self.dialogues = npc.dialogue
        print(f"Dialogues: {self.dialogues}")
        print(f"Dialogue 0: {self.dialogues[0].text}")
        self.dialogue_index = 0
        self.sub_dialogue_index = 0
        self.total_dialogues = len(self.dialogues)

    def start_dialogue(self):
        self.sub_dialogue_index = self.npc.dialogue[self.dialogue_index].current_text_index
        current_text_index = self.npc.dialogue[self.dialogue_index].current_text_index
        dialogue_text = self.dialogues[self.dialogue_index].text[current_text_index]
        self.dialogue_box.create_dialogue(dialogue_text, self.sub_dialogue_index, self.total_dialogues)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.dialogue_box.close_button_rect and self.dialogue_box.close_button_rect.collidepoint(event.pos):
                self.dialogue_box.show = False
            elif self.dialogue_box.prev_button_rect and self.dialogue_box.prev_button_rect.collidepoint(event.pos):
                # self.current_dialogue_index = max(self.current_dialogue_index - 1, 0)
                self.npc.dialogue[self.dialogue_index].point_to_previous_text()
                print(f"Current dialogue index: {self.npc.dialogue[self.dialogue_index].current_text_index}")
                self.start_dialogue()
            elif self.dialogue_box.next_button_rect and self.dialogue_box.next_button_rect.collidepoint(event.pos):
                # self.current_dialogue_index = min(self.current_dialogue_index + 1, self.total_dialogues - 1)
                self.npc.dialogue[self.dialogue_index].point_to_next_text()
                print(f"Current dialogue index: {self.npc.dialogue[self.dialogue_index].current_text_index}")
                self.start_dialogue()

    def pick_random_dialogue(self):
        self.dialogue_index = random.randint(0, self.total_dialogues - 1)
        self.start_dialogue()