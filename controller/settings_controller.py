import pygame, sys

class SettingsController:
    def __init__(self, model, view):
        self.model = model
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
                    elif self.view.respawn_mobs_button_rect.collidepoint(event.pos):
                        self.handle_respawn_mobs()
                    elif self.view.reset_quests_button_rect.collidepoint(event.pos):
                        self.handle_reset_quests()
                    elif self.view.reset_items_button_rect.collidepoint(event.pos):
                        self.handle_reset_items()

                self.view.display_settings()

    def handle_respawn_mobs(self):
        # Add logic to respawn mobs
        pass

    def handle_reset_quests(self):
        # Add logic to reset quests
        pass

    def handle_reset_items(self):
        # Add logic to reset items
        pass
