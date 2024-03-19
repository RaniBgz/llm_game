import pygame
from view import view_constants as view_cst


class MainGameView:
    def __init__(self, screen):
        self.screen = screen
        self.button_font = pygame.font.SysFont("Arial", 25)
        self.quests_text = self.button_font.render("Quests", True, view_cst.TEXT_COLOR)
        self.world_text = self.button_font.render("World", True, view_cst.TEXT_COLOR)
        self.inventory_text = self.button_font.render("Inventory", True, view_cst.TEXT_COLOR)
        self.map_text = self.button_font.render("Map", True, view_cst.TEXT_COLOR)

        button_width = view_cst.WIDTH // 4  # Divide the screen width into 4 segments
        x_offset = button_width // 2  # For initial button centering within the segment
        button_height = 40
        button_y = view_cst.HEIGHT - button_height - 10  # Position buttons 10 pixels above the bottom

        # Calculate button positions with appropriate spacing
        self.quests_rect = self.quests_text.get_rect(center=(x_offset, button_y))
        self.inventory_rect = self.inventory_text.get_rect(center=(x_offset + button_width, button_y))
        self.map_rect = self.map_text.get_rect(center=(x_offset + 2 * button_width, button_y))
        self.world_rect = self.world_text.get_rect(center=(x_offset + 3 * button_width, button_y))

    def draw(self):
        self.screen.fill(view_cst.WHITE)
        self.screen.blit(self.quests_text, self.quests_rect)
        self.screen.blit(self.inventory_text, self.inventory_rect)
        self.screen.blit(self.map_text, self.map_rect)
        self.screen.blit(self.world_text, self.world_rect)
        pygame.display.flip()
