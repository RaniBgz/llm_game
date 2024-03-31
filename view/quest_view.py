import pygame
from view import view_constants as view_cst



class QuestView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 20)
        self.exit_button_text = self.font.render("X", True, view_cst.TEXT_COLOR)
        self.exit_button_rect = self.exit_button_text.get_rect(topright=(view_cst.WIDTH - 10, 10))

    def display_quests(self, quests):
        self.screen.fill(view_cst.WHITE)

        # Title
        title_text = self.font.render("Quests", True, view_cst.TEXT_COLOR)
        title_rect = title_text.get_rect(center=(view_cst.WIDTH // 2, 20))
        self.screen.blit(title_text, title_rect)

        # Display quests
        y = 50
        for quest in quests:
            if quest.active:
                color = view_cst.RED
            if quest.completed:
                color = view_cst.GREEN
            else:
                color = view_cst.TEXT_COLOR
            quest_text = self.font.render(quest.name, True, color)
            self.screen.blit(quest_text, (20, y))
            y += 30

        # Exit Button
        self.screen.blit(self.exit_button_text, self.exit_button_rect)

        pygame.display.flip()