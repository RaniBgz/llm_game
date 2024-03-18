import sys
import pygame

class MainMenuController:
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
                    if self.view.play_rect.collidepoint(event.pos):
                         self.start_game()

            self.view.display_menu()

    def start_game(self):
        pass
        # ... Logic to transition to MainGameController