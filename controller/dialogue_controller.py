import pygame
import random
from model.dialogue import Dialogue

#TODO: Revamp all of this to make it much simpler to access: the right dialogue, the right index in the dialogue, and update between text
#TODO: The Dialoge Controller may have too much information. It only needs to know the current Dialogue.
#TODO: Need to add logic "en amont" to check if the dialogue is a quest or a chat, and find out if the NPC has a (non-given) quest to give.
class DialogueController:
    def __init__(self, screen, dialogue_box, npc, character, dialogue, dialogue_type="chat"):
        self.screen = screen
        self.dialogue_box = dialogue_box
        self.npc = npc
        self.character = character
        self.dialogue = dialogue
        self.dialogue_type = dialogue_type
        self.dialogue_length = self.dialogue.get_dialogue_length()

    def start_dialogue(self):
        self.dialogue_index = self.dialogue.current_text_index
        dialogue_text = self.dialogue.get_current_dialogue()
        print(f"Dialogue index is {self.dialogue_index} and dialogue length is {self.dialogue_length}")
        self.dialogue_box.create_dialogue(self.npc.name, dialogue_text)
        if(self.dialogue_index == self.dialogue_length - 1) and self.dialogue_type == "quest":
            self.dialogue_box.create_accept_decline_buttons()

    def reset_dialogue(self):
        self.dialogue.current_text_index = 0
        self.dialogue_length = self.dialogue.get_dialogue_length()
        self.dialogue_box.show = False

    #TODO: Reset things on close
    #TODO: From outside scope, may need to destroy the dialogue controller and other objects
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.dialogue_box.close_button_rect and self.dialogue_box.close_button_rect.collidepoint(event.pos):
                # self.dialogue_box.show = False
                self.reset_dialogue()
            elif self.dialogue_box.prev_button_rect and self.dialogue_box.prev_button_rect.collidepoint(event.pos):
                print("Position clicked: ", event.pos)
                print(f"Dialogue index before pointing to previous text: {self.dialogue.current_text_index}")
                self.dialogue.point_to_previous_text()
                print(f"Dialogue index after pointing to previous text: {self.dialogue.current_text_index}")
                self.start_dialogue()
            elif self.dialogue_box.next_button_rect and self.dialogue_box.next_button_rect.collidepoint(event.pos):
                print("Position clicked: ", event.pos)
                print(f"Dialogue index before pointing to next text: {self.dialogue.current_text_index}")
                self.dialogue.point_to_next_text()
                print(f"Dialogue index after pointing to next text: {self.dialogue.current_text_index}")
                self.start_dialogue()
            if self.dialogue_type == "quest":
                if self.dialogue_box.accept_button_rect and self.dialogue_box.accept_button_rect.collidepoint(event.pos):
                    print("Accept button clicked")
                    # Add your logic here for accepting the quest
                    self.reset_dialogue()
                    return "accept_quest"
                elif self.dialogue_box.decline_button_rect and self.dialogue_box.decline_button_rect.collidepoint(event.pos):
                    print("Decline button clicked")
                    # Add your logic here for declining the quest
                    self.reset_dialogue()
                    return "decline_quest"

