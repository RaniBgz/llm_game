import pygame
from view.ui.popup_box import PopupBox
from view import view_constants as view_cst
from view.ui import utils

class ItemInfoBox(PopupBox):
    def __init__(self, screen):
        width, height = 200, 100
        super().__init__(screen, width, height)
        self.item = None
        self.item_rect = None
        self.font = pygame.font.SysFont("Arial", 16)
        self.exit_font = pygame.font.SysFont("Arial", 32)

    def create_item_info(self, item, item_rect):
        self.item = item

        screen_width, screen_height = pygame.display.get_surface().get_size()
        if item_rect.width + item_rect[0] + self.width < screen_width:
            print("Enough space to the right")
            self.rect.midleft = (item_rect.midright[0] + 10, item_rect.midright[1])
        else:
            print("Not enough space to the right")
            self.rect.midright = (item_rect.midleft[0] - 10, item_rect.midleft[1])

        self.surface.fill(view_cst.POPUP_BG_COLOR)

        item_name = f"{self.item.name}"
        item_name_text = self.font.render(item_name, True, view_cst.TEXT_COLOR)
        self.surface.blit(item_name_text, (10, 10))

        # Render the item description with word wrapping
        item_description = f"{self.item.description}"
        description_width = self.rect.width - 20  # Subtract padding from both sides
        item_description_lines = [line.strip() for line in item_description.split('\n')]  # Split into lines
        y = 30
        for line in item_description_lines:
            wrapped_lines = utils.wrap_text(line, description_width, view_cst.TEXT_COLOR)
            for wrapped_line in wrapped_lines:
                self.surface.blit(wrapped_line, (10, y))
                y += wrapped_line.get_height()

        self.create_close_button(self.exit_font, view_cst.TEXT_COLOR)
        self.show = True

    def create_close_button(self, font, color):
        close_button_text = font.render("X", True, color)
        close_button_rect = close_button_text.get_rect(topright=(self.width - 10, 10))
        pygame.draw.rect(self.surface, view_cst.POPUP_BG_COLOR, close_button_rect)
        self.surface.blit(close_button_text, close_button_rect)
        self.close_button_rect = pygame.Rect(self.rect.topright[0] - 40, self.rect.topright[1], 40, 40)


    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_button_rect and self.close_button_rect.collidepoint(event.pos):
                self.show = False
