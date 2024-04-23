import pygame
import random
from model.dialogue.dialogue import Dialogue
from view import view_constants as view_cst

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
        self.set_npc_type()
        self.generate_quest_button_visible = True

    def set_npc_type(self):
        if self.npc.robot:
            print(f"NPC is a robot")
            self.npc_type = "robot"
            self.dialogue_box.set_background_color(view_cst.LIGHT_GRAY)
            self.dialogue_box.set_name_color(view_cst.SCI_FI_BLUE_5)
        else:
            print(f"NPC is a human")
            self.npc_type = "human"
            self.dialogue_box.set_background_color(view_cst.PARCHMENT_COLOR)
            self.dialogue_box.set_name_color(view_cst.COFFEE_BROWN_3)


    def start_dialogue(self):
        self.dialogue_index = self.dialogue.get_current_text_index()
        dialogue_text = self.dialogue.get_current_dialogue()
        print(f"Dialogue index is {self.dialogue_index} and dialogue length is {self.dialogue_length}")
        self.dialogue_box.create_dialogue(self.npc.name, dialogue_text)
        if self.npc_type == "robot":
            self.handle_generate_quest_button_logic()
        self.handle_prev_next_buttons_logic()
        self.handle_quest_buttons_logic()


    def reset_dialogue(self):
        self.dialogue.current_text_index = 0
        self.dialogue_length = self.dialogue.get_dialogue_length()
        self.dialogue_box.show = False

    def handle_prev_next_buttons_logic(self):
        if self.dialogue_index == 0:
            if self.dialogue_length == 1:
                return
            else:
                self.dialogue_box.create_next_button()
        elif self.dialogue_index == self.dialogue_length - 1:
            self.dialogue_box.create_prev_button()
        else:
            self.dialogue_box.create_prev_button()
            self.dialogue_box.create_next_button()

    def handle_quest_buttons_logic(self):
        if(self.dialogue_index == self.dialogue_length - 1) and self.dialogue_type == "quest_initialization":
            self.dialogue_box.create_accept_decline_buttons()
        if(self.dialogue_index == self.dialogue_length - 1) and self.dialogue_type == "quest_completion":
            self.dialogue_box.create_end_quest_button()

    def handle_generate_quest_button_logic(self):
        if self.dialogue_index == 0 and self.generate_quest_button_visible:
            print(f"Calling create generate quest button")
            self.dialogue_box.create_generate_quest_button()
        else:
            print(f"Calling hide generate quest button")
            self.dialogue_box.hide_generate_quest_button()

    def handle_events(self, event):
        print(f"In dialogue controller event")
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.dialogue_box.close_button_rect and self.dialogue_box.close_button_rect.collidepoint(event.pos):
                self.reset_dialogue()
            elif getattr(self.dialogue_box, 'prev_button_rect', None) and self.dialogue_box.prev_button_rect.collidepoint(event.pos):
                self.dialogue.point_to_previous_text()
                self.start_dialogue()
            elif getattr(self.dialogue_box, 'next_button_rect', None) and self.dialogue_box.next_button_rect.collidepoint(event.pos):
                self.dialogue.point_to_next_text()
                self.start_dialogue()
            elif getattr(self.dialogue_box, 'generate_quest_button_rect', None) and self.dialogue_box.generate_quest_button_rect.collidepoint(event.pos):
                print(f"Generating quest button clicked")
                self.generate_quest_button_visible = False
                self.handle_generate_quest_button_logic()
                return "generate_quest"
            if self.dialogue_type == "quest_initialization":
                if getattr(self.dialogue_box, 'accept_button_rect', None) and self.dialogue_box.accept_button_rect.collidepoint(event.pos):
                    self.reset_dialogue()
                    return "accept_quest"
                elif getattr(self.dialogue_box, 'decline_button_rect', None) and  self.dialogue_box.decline_button_rect.collidepoint(event.pos):
                    self.reset_dialogue()
                    return "decline_quest"
            if self.dialogue_type == "quest_completion":
                if getattr(self.dialogue_box, 'end_quest_button_rect', None) and self.dialogue_box.end_quest_button_rect.collidepoint(event.pos):
                    self.reset_dialogue()
                    return "end_quest"

