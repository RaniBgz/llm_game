import sys
import pygame

class QuestController:
    def __init__(self, game_data, view):
        self.game_data = game_data
        self.view = view

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.view.exit_button_rect.collidepoint(event.pos):
                        running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            self.view.display_quests(self.game_data.character.quests)