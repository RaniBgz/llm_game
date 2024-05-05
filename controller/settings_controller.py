import pygame, sys

class SettingsController:
    def __init__(self, game_data, view):
        self.game_data = game_data
        self.view = view

    def run(self):
        running = True
        while running:
            self.view.render()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_events(event)  # Handle all events
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False


    def handle_respawn_mobs(self):
        self.game_data.respawn_mobs()

    def handle_reset_quests(self):
        self.game_data.reset_quests()
        pass

    def handle_reset_items(self):
        self.game_data.reset_items()
        # Add logic to reset items
        pass
