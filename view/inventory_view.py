import pygame
from view import view_constants as view_cst
from model import settings as settings


class InventoryView:
    def __init__(self, screen):
        self.screen = screen
        self.item_image_dims = (80,80)
        self.title_font = pygame.font.SysFont("Arial", 32)
        self.font = pygame.font.SysFont("Arial", 24)
        self.exit_font = pygame.font.SysFont("Arial", 30)
        self.exit_button_text = self.exit_font.render("X", True, view_cst.TEXT_COLOR)
        self.exit_button_rect = self.exit_button_text.get_rect(topright=(view_cst.WIDTH - 10, 10))  # Top right corner

    def display_inventory(self, inventory):
        self.screen.fill(view_cst.LIGHT_GRAY)

        # Title
        title_text = self.title_font.render("Inventory", True, view_cst.TEXT_COLOR)
        title_rect = title_text.get_rect(center=(view_cst.WIDTH // 2, 40))
        self.screen.blit(title_text, title_rect)

        # Display items
        y = 50  # Start below the title
        space_between_items = 25  # Increased space between items
        for item in inventory:
            # Load and display the item image
            item_image = pygame.image.load(item.sprite).convert_alpha()
            item_image = pygame.transform.scale(item_image, self.item_image_dims)
            item_rect = item_image.get_rect(topleft=(20, y))
            self.screen.blit(item_image, item_rect)

            # Display the item name next to the image
            item_text = self.font.render(f"{item.name}", True, (0, 0, 0))
            text_x = item_rect.right + 40  # Add some padding between the image and the text
            self.screen.blit(item_text, (text_x, y + item_rect.height // 2 - item_text.get_height() // 2))

            y += item_rect.height + space_between_items  # Move y down for the next item

        # Exit Button
        self.screen.blit(self.exit_button_text, self.exit_button_rect)

        pygame.display.flip()


    # def display_inventory(self, inventory):
    #      self.screen.fill(view_cst.WHITE)
    #
    #      # Title
    #      title_text = self.font.render("Inventory", True, view_cst.TEXT_COLOR)
    #      title_rect = title_text.get_rect(center=(view_cst.WIDTH // 2, 20))
    #      self.screen.blit(title_text, title_rect)
    #
    #      # Display items
    #      y = 50  # Start below the title
    #      for item in inventory:
    #          item_text = self.font.render(f"{item.name}", True, (0, 0, 0))
    #          self.screen.blit(item_text, (20, y))
    #          y += 30  # Space between items
    #
    #      # Exit Button
    #      self.screen.blit(self.exit_button_text, self.exit_button_rect)
    #
    #      pygame.display.flip()
