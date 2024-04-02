import sys
import pygame

class QuestController:
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
                    if self.view.exit_button_rect.collidepoint(event.pos):
                        return  # Return to the main game

            self.view.display_quests(self.game_data.character.quests)