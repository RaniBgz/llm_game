import pygame

WIDTH, HEIGHT = 640, 480
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class InventoryView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 20)
        self.exit_button_text = self.font.render("X", True, RED)
        self.exit_button_rect = self.exit_button_text.get_rect(topright=(WIDTH - 10, 10))  # Top right corner

    def display_inventory(self, inventory):
         self.screen.fill(WHITE)

         # Title
         title_text = self.font.render("Inventory", True, RED)
         title_rect = title_text.get_rect(center=(WIDTH // 2, 20))
         self.screen.blit(title_text, title_rect)

         # Display items
         y = 50  # Start below the title
         for item in inventory:
             item_text = self.font.render(f"- {item.name}", True, (0, 0, 0))
             self.screen.blit(item_text, (20, y))
             y += 30  # Space between items

         # Exit Button
         self.screen.blit(self.exit_button_text, self.exit_button_rect)

         pygame.display.flip()