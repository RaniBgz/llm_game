import pygame, sys

class SettingsController:
    def __init__(self, game_data, view):
        self.game_data = game_data
        self.view = view

    def run(self):
        self.running = True
        while self.running:
            self.view.render()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_events(event)  # Handle all events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down_event(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up_event(event)

    def handle_mouse_down_event(self, event):
        if self.view.back_button_rect.collidepoint(event.pos):
            self.running = False  # Set a flag to exit the Settings loop
            return  # Stop processing other events
        # Check which button, if any, was clicked
        for button_name in ['respawn_mobs_button', 'reset_quests_button', 'reset_items_button']:
            button = getattr(self.view, button_name, None)
            if button and button.is_clicked(event):
                self.pressed_button = button_name  # Mark the button as pressed
                button.handle_mouse_down()  # Change button appearance
                break  # We found the button, stop the loop

    def handle_mouse_up_event(self, event):
        button_to_call = None
        # Check which button, if any, is released
        for button_name in ['respawn_mobs_button', 'reset_quests_button', 'reset_items_button']:
            button = getattr(self.view, button_name, None)
            if button and button.is_clicked(event) and self.pressed_button == button_name:
                button.handle_mouse_up()  # Change button appearance back
                button_to_call = button_name  # Remember which button to action
                break
        # If no button matches, reset all
        if not button_to_call:
            self.reset_all_buttons()

        self.handle_button_action(button_to_call)

        self.pressed_button = None  # Reset the pressed flag

    def handle_button_action(self, button_to_call):
        if button_to_call == 'respawn_mobs_button':
            self.handle_respawn_mobs()
        elif button_to_call == 'reset_quests_button':
            self.handle_reset_quests()
        elif button_to_call == 'reset_items_button':
            self.handle_reset_items()

    def reset_all_buttons(self):
        for button_name in ['respawn_mobs_button', 'reset_quests_button', 'reset_items_button']:
            button = getattr(self.view, button_name, None)
            if button:
                button.handle_mouse_up()  # Reset appearance

    def handle_respawn_mobs(self):
        self.game_data.respawn_mobs()

    def handle_reset_quests(self):
        self.game_data.reset_quests()
        pass

    def handle_reset_items(self):
        self.game_data.reset_items()
        pass
