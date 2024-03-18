import pygame

WIDTH, HEIGHT = 640, 480
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class QuestView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 20)
        self.exit_button_text = self.font.render("X", True, RED)
        self.exit_button_rect = self.exit_button_text.get_rect(topright=(WIDTH - 10, 10))

    def display_quests(self, quests):
        self.screen.fill(WHITE)

        # Title
        title_text = self.font.render("Quests", True, RED)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 20))
        self.screen.blit(title_text, title_rect)

        # Display quests
        y = 50
        for quest in quests:
            color = RED if quest.active else (0, 0, 0)  # Red for active, black otherwise
            quest_text = self.font.render(quest.name, True, color)
            self.screen.blit(quest_text, (20, y))
            y += 30

        # Exit Button
        self.screen.blit(self.exit_button_text, self.exit_button_rect)

        pygame.display.flip()