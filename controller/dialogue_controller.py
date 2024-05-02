import pygame
import asyncio
import random
from model.dialogue.dialogue import Dialogue
from view import view_constants as view_cst

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
        self.button_flags = {
            "generate_quest": False,
            "accept_quest": False,
            "decline_quest": False,
            "end_quest": False,
            "prev": False,
            "next": False
        }
        self.button_displayed = {
            "generate_quest": False,
            "accept_quest": False,
            "decline_quest": False,
            "end_quest": False,
            "prev": False,
            "next": False
        }

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
        self.dialogue_index = self.dialogue.get_current_text_index() #Get current dialogue index
        print(f"Dialogue index: {self.dialogue_index}")
        self.dialogue_text = self.dialogue.get_current_dialogue() #Setting dialogue text to display
        if self.npc_type == "robot":
            self.handle_generate_quest_button_logic()
        self.handle_prev_next_buttons_logic()
        self.handle_quest_buttons_logic()


    def render_dialogue_box(self):
        #Render each button when it has to be rendered, skip if it's not
        self.dialogue_box.create_dialogue(self.npc.name, self.dialogue_text)
        #TODO: Handle draw vs create depending on situation
        if self.button_displayed["prev"]:
            self.dialogue_box.create_prev_button()
        if self.button_displayed["next"]:
            self.dialogue_box.create_next_button()
        if self.button_displayed["generate_quest"]:
            self.dialogue_box.create_generate_quest_button()
        if self.button_displayed["accept_quest"] and self.button_displayed["decline_quest"]:
            self.dialogue_box.create_accept_decline_buttons()
        if self.button_displayed["end_quest"]:
            self.dialogue_box.create_end_quest_button()

    def reset_dialogue(self):
        self.dialogue.current_text_index = 0
        self.dialogue_length = self.dialogue.get_dialogue_length()
        self.dialogue_box.show = False

    #TODO: fix that, the buttons are probably not created properly
    #TODO: add button flags
    def handle_prev_next_buttons_logic(self):
        if self.dialogue_index == 0:
            if self.dialogue_length == 1:
                self.button_displayed["prev"] = False
                self.button_displayed["next"] = False
                return
            else:
                self.button_displayed["prev"] = False
                self.button_displayed["next"] = True

        elif self.dialogue_index == self.dialogue_length - 1:
            self.button_displayed["prev"] = True
            self.button_displayed["next"] = False

        else:
            self.button_displayed["prev"] = True
            self.button_displayed["next"] = True


    def handle_quest_buttons_logic(self):
        if(self.dialogue_index == self.dialogue_length - 1) and self.dialogue_type == "quest_initialization":
            self.button_displayed["accept_quest"] = True
            self.button_displayed["decline_quest"] = True
            # self.dialogue_box.create_accept_decline_buttons()
        if(self.dialogue_index == self.dialogue_length - 1) and self.dialogue_type == "quest_completion":
            self.button_displayed["end_quest"] = True
            # self.dialogue_box.create_end_quest_button()

    def handle_generate_quest_button_logic(self):
        if self.dialogue_index == 0 and self.generate_quest_button_visible:
            self.button_displayed["generate_quest"] = True
        else:
            self.button_displayed["generate_quest"] = False

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            return_code = self.handle_mouse_up(event)
            if return_code:
                return return_code

    def handle_mouse_down(self, event):
        if self.dialogue_box.close_button_rect and self.dialogue_box.close_button_rect.collidepoint(event.pos):
            self.reset_dialogue()
        if getattr(self.dialogue_box, 'prev_button', None): #Check prev button exists
            if self.dialogue_box.prev_button.is_clicked(event):
                self.dialogue_box.prev_button.handle_mouse_down(event) #Change button image to pressed
                print(f"Prev button clicked")
                self.button_flags["prev"] = True #Set prev flag to true
        if getattr(self.dialogue_box, 'next_button', None): #Check next button exists
            if self.dialogue_box.next_button.is_clicked(event):
                self.dialogue_box.next_button.handle_mouse_down(event) #Change button image to pressed
                print(f"Next button clicked")
                self.button_flags["next"] = True #Set next flag to true
        if getattr(self.dialogue_box, 'generate_quest_button', None):
            if self.dialogue_box.generate_quest_button.is_clicked(event):
                self.dialogue_box.generate_quest_button.handle_mouse_down(event)
                print(f"Generate quest button clicked")
                self.button_flags["generate_quest"] = True
        if getattr(self.dialogue_box, 'accept_button', None):
            if self.dialogue_box.accept_button.is_clicked(event):
                self.dialogue_box.accept_button.handle_mouse_down(event)
                print(f"Accept button clicked")
                self.button_flags["accept_quest"] = True
        if getattr(self.dialogue_box, 'decline_button', None):
            if self.dialogue_box.decline_button.is_clicked(event):
                self.dialogue_box.decline_button.handle_mouse_down(event)
                print(f"Decline button clicked")
                self.button_flags["decline_quest"] = True
        if getattr(self.dialogue_box, 'end_quest_button', None):
            if self.dialogue_box.end_quest_button.is_clicked(event):
                self.dialogue_box.end_quest_button.handle_mouse_down(event)
                print(f"End quest button clicked")
                self.button_flags["end_quest"] = True


    def handle_mouse_up(self, event):
        if getattr(self.dialogue_box, 'prev_button', None):
            if self.dialogue_box.prev_button.is_clicked(event):
                if self.button_flags["prev"]:
                    print(f"Prev button released")
                    self.dialogue_box.prev_button.handle_mouse_up(event)  # Changes the button image back to normal
                    self.dialogue.point_to_previous_text()  # Point to previous text
                    self.start_dialogue()  # Start dialogue
        if getattr(self.dialogue_box, 'next_button', None):
            if self.dialogue_box.next_button.is_clicked(event):
                if self.button_flags["next"]:
                    print(f"Next button released")
                    self.dialogue_box.next_button.handle_mouse_up(event)
                    self.dialogue.point_to_next_text()  # Point to next text
                    self.start_dialogue()  # Start dialogue
        if getattr(self.dialogue_box, 'generate_quest_button', None):
            if self.dialogue_box.generate_quest_button.is_clicked(event):
                if self.button_flags["generate_quest"]:
                    print(f"Generate quest button released")
                    self.dialogue_box.generate_quest_button.handle_mouse_up(event)
                    self.generate_quest_button_visible = False
                    return "generate_quest"
        if getattr(self.dialogue_box, 'accept_button', None):
            if self.dialogue_box.accept_button.is_clicked(event):
                if self.button_flags["accept_quest"]:
                    print(f"Accept button released")
                    self.dialogue_box.accept_button.handle_mouse_up(event)
                    self.reset_dialogue()
                    return "accept_quest"
        if getattr(self.dialogue_box, 'decline_button', None):
            if self.dialogue_box.decline_button.is_clicked(event):
                if self.button_flags["decline_quest"]:
                    print(f"Decline button released")
                    self.dialogue_box.decline_button.handle_mouse_up(event)
                    self.reset_dialogue()
                    return "decline_quest"
        if getattr(self.dialogue_box, 'end_quest_button', None):
            if self.dialogue_box.end_quest_button.is_clicked(event):
                if self.button_flags["end_quest"]:
                    print(f"End quest button released")
                    self.dialogue_box.end_quest_button.handle_mouse_up(event)
                    self.reset_dialogue()
                    return "end_quest"

        for flag in self.button_flags: #Reset all flags
            self.button_flags[flag] = False
