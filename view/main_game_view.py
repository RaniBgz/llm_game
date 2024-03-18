import pygame

WIDTH, HEIGHT = 640, 480
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class MainGameView:
    def __init__(self, screen):
        self.screen = screen
        self.button_font = pygame.font.SysFont("Arial", 25)
        self.quests_text = self.button_font.render("Quests", True, RED)
        self.world_text = self.button_font.render("World", True, RED)
        self.inventory_text = self.button_font.render("Inventory", True, RED)
        self.map_text = self.button_font.render("Map", True, RED)

        button_width = WIDTH // 4  # Divide the screen width into 4 segments
        x_offset = button_width // 2  # For initial button centering within the segment
        button_height = 40
        button_y = HEIGHT - button_height - 10  # Position buttons 10 pixels above the bottom

        # Calculate button positions with appropriate spacing
        self.quests_rect = self.quests_text.get_rect(center=(x_offset, button_y))
        self.inventory_rect = self.inventory_text.get_rect(center=(x_offset + button_width, button_y))
        self.map_rect = self.map_text.get_rect(center=(x_offset + 2 * button_width, button_y))
        self.world_rect = self.world_text.get_rect(center=(x_offset + 3 * button_width, button_y))

    def draw(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.quests_text, self.quests_rect)
        self.screen.blit(self.inventory_text, self.inventory_rect)
        self.screen.blit(self.map_text, self.map_rect)
        self.screen.blit(self.world_text, self.world_rect)
        pygame.display.flip()
