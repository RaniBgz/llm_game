import pygame
import view.view_constants as view_cst
from view.quest_view import QuestView
from view.inventory_view import InventoryView
from view.map_view import MapView
from controller.quest_controller import QuestController
from controller.inventory_controller import InventoryController
from controller.map_controller import MapController

class GameMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.menu_items = [
            "Quests",
            "Inventory",
            "Map"
        ]
        self.create_menu_buttons()

    def create_menu_buttons(self):
        self.buttons = []
        button_width = view_cst.WIDTH // len(self.menu_items) + 1
        button_height = 2*view_cst.TILE_HEIGHT//3
        button_y = view_cst.HEIGHT - button_height #- 10


        button_color = view_cst.DARK_GRAY
        button_hover_color = view_cst.LIGHT_GRAY
        text_color = view_cst.SCI_FI_BLUE_3
        button_border_color = view_cst.DARK_GRAY_2
        button_border_width = 2

        for i, item in enumerate(self.menu_items):
            # Render the button surface with the metallic color and border
            button_rect = pygame.Rect((i * button_width, button_y), (button_width, button_height))
            button_surface = pygame.Surface(button_rect.size)
            button_surface.fill(button_color)
            pygame.draw.rect(button_surface, button_border_color, button_surface.get_rect(), button_border_width)

            # Render the text on the button
            text = self.font.render(item, True, text_color)
            text_rect = text.get_rect(center=button_rect.center)

            # Add the button and text to the list of buttons
            self.buttons.append((button_surface, button_rect, text, text_rect, button_hover_color))


        # for i, item in enumerate(self.menu_items):
        #     text = self.font.render(item, True, view_cst.TEXT_COLOR)
        #     rect = text.get_rect(center=((i + 0.5) * button_width, button_y))
        #     self.buttons.append((text, rect))

    def display(self):
        for button_surface, button_rect, text, text_rect, _ in self.buttons:
            self.screen.blit(button_surface, button_rect)
            self.screen.blit(text, text_rect)
        # for text, rect in self.buttons:
        #     self.screen.blit(text, rect)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button_surface, button_rect, text, text_rect, button_hover_color in self.buttons:
                if button_rect.collidepoint(event.pos):
                    # Handle menu item click event
                    menu_item_clicked = self.menu_items[self.buttons.index((button_surface, button_rect, text, text_rect, button_hover_color))]
                    if menu_item_clicked == "Quests":
                        return view_cst.QUEST_MENU
                    elif menu_item_clicked == "Inventory":
                        return view_cst.INVENTORY_MENU
                    elif menu_item_clicked == "Map":
                        return view_cst.MAP_MENU
            # for text, rect in self.buttons:
            #     if rect.collidepoint(event.pos):
            #         # Handle menu item click event
            #         menu_item_clicked = self.menu_items[self.buttons.index((text, rect))]
            #         if menu_item_clicked == "Quests":
            #             return view_cst.QUEST_MENU
            #         elif menu_item_clicked == "Inventory":
            #             return view_cst.INVENTORY_MENU
            #         elif menu_item_clicked == "Map":
            #             return view_cst.MAP_MENU
        # elif event.type == pygame.MOUSEMOTION:
        #     for button_surface, button_rect, text, text_rect, button_hover_color in self.buttons:
        #         if button_rect.collidepoint(event.pos):
        #             # Highlight the button on hover
        #             button_surface.fill(button_hover_color)
        #             pygame.draw.rect(button_surface, button_border_color, button_surface.get_rect(), button_border_width)
        #             self.screen.blit(button_surface, button_rect)
        #             self.screen.blit(text, text_rect)
        #         else:
        #             # Reset the button to its original color
        #             button_surface.fill(button_color)
        #             pygame.draw.rect(button_surface, button_border_color, button_surface.get_rect(), button_border_width)
        #             self.screen.blit(button_surface, button_rect)
        #             self.screen.blit(text, text_rect)
