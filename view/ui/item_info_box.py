import pygame
from view.ui.popup_box import PopupBox
from view import view_constants as view_cst
from view.ui import utils

class ItemInfoBox(PopupBox):
    def __init__(self, screen, item, item_rect):
        width, height = 200, 100
        super().__init__(screen, width, height)
        self.item = item
        self.rect.midleft = (item_rect.midright[0] + 10, item_rect.midright[1])
        self.create_item_info()

    def create_item_info(self):
        font = pygame.font.SysFont("Arial", 16)
        self.surface.fill(view_cst.POPUP_BG_COLOR)

        item_name = f"{self.item.name}"
        item_name_text = font.render(item_name, True, view_cst.TEXT_COLOR)
        self.surface.blit(item_name_text, (10, 10))

        # Render the item description with word wrapping
        item_description = f"{self.item.description}"
        description_width = self.rect.width - 20  # Subtract padding from both sides
        item_description_lines = [line.strip() for line in item_description.split('\n')]  # Split into lines
        y = 30
        for line in item_description_lines:
            # line_text = font.render(line, True, view_cst.TEXT_COLOR)
            wrapped_lines = utils.wrap_text(line, description_width)
            for wrapped_line in wrapped_lines:
                self.surface.blit(wrapped_line, (10, y))
                y += wrapped_line.get_height()

        # item_description = f"{self.item.description}"
        # item_description_text = font.render(item_description, True, view_cst.TEXT_COLOR)
        # self.surface.blit(item_description_text, (10, 30))

        #TODO: Add value to items

        # npc_hostile = "Hostile" if self.npc.hostile else "Friendly"
        # txt_color = view_cst.RED if self.npc.hostile else view_cst.GREEN
        # npc_hostile_text = font.render(npc_hostile, True, txt_color)
        # self.surface.blit(npc_hostile_text, (10, 50))

        self.create_close_button(font, view_cst.TEXT_COLOR)