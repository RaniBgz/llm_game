import pygame
from view import view_constants as view_cst

class SettingsView:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 30)

        # Title
        self.title_text = self.font.render("Settings", True, view_cst.TEXT_COLOR)
        self.title_rect = self.title_text.get_rect(center=(view_cst.WIDTH // 2, view_cst.HEIGHT // 4))

        # Back button
        self.back_button_text = self.font.render("Back", True, view_cst.TEXT_COLOR)
        self.back_button_rect = self.back_button_text.get_rect(topright=(view_cst.WIDTH - 10, 10))

        # Button colors
        self.button_color = view_cst.DARK_GRAY
        self.button_hover_color = view_cst.LIGHT_GRAY
        self.text_color = view_cst.SCI_FI_BLUE_3
        self.button_border_color = view_cst.DARK_GRAY_2
        self.button_border_width = 2

        # Menu items
        self.menu_items = ["Respawn Mobs", "Reset Quests", "Reset Items"]

        # Buttons
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        button_width = view_cst.WIDTH // 3  # Fixed width for all buttons
        button_height = 40  # Adjust the height of the buttons as needed
        button_spacing = 20  # Adjust the spacing between buttons
        start_y = view_cst.HEIGHT // 2 - (len(self.menu_items) * (button_height + button_spacing)) // 2

        for i, item in enumerate(self.menu_items):
            button_y = start_y + i * (button_height + button_spacing)
            button_rect = pygame.Rect((view_cst.WIDTH // 2 - button_width // 2, button_y), (button_width, button_height))
            button_surface = pygame.Surface(button_rect.size)
            button_surface.fill(self.button_color)
            pygame.draw.rect(button_surface, self.button_border_color, button_surface.get_rect(), self.button_border_width)

            # Render the text on the button
            text = self.font.render(item, True, self.text_color)
            text_rect = text.get_rect(center=button_rect.center)

            # Add the button and text to the list of buttons
            self.buttons.append((button_surface, button_rect, text, text_rect))

    def display_settings(self):
        self.screen.fill(view_cst.WHITE)
        self.screen.blit(self.title_text, self.title_rect)
        self.screen.blit(self.back_button_text, self.back_button_rect)

        for button in self.buttons:
            self.screen.blit(button[0], button[1])
            self.screen.blit(button[2], button[3])

        pygame.display.flip()
