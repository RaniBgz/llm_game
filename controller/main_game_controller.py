import sys
import pygame

class MainGameController:
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
                    pass
                     # ... Handle button clicks for quests, inventory, etc.

            self.view.display_game_ui()