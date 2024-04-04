import pygame, sys

class SettingsController:
    def __init__(self, game_data, view):
        self.game_data = game_data
        self.view = view

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.view.back_button_rect.collidepoint(event.pos):
                        return
                    else:
                        button_index = self.view.handle_events(event)
                        if button_index is not None:
                            self.handle_selected_button(button_index)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.view.reset_selected_button()
                self.view.display_settings()

    def handle_selected_button(self, button_index):
        print(f"Selected button index: {button_index}")
        if button_index == 0:  # Respawn Mobs
            print(f"Clicked respawn mobs button")
            self.handle_respawn_mobs()
        elif button_index == 1:  # Reset Quests
            self.handle_reset_quests()
        elif button_index == 2:  # Reset Items
            self.handle_reset_items()

    def handle_respawn_mobs(self):
        self.game_data.respawn_mobs()

    def handle_reset_quests(self):
        self.game_data.reset_quests()
        pass

    def handle_reset_items(self):
        self.game_data.reset_items()
        # Add logic to reset items
        pass
