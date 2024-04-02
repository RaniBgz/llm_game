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
        button_width = view_cst.WIDTH // len(self.menu_items)
        button_height = 40
        button_y = view_cst.HEIGHT - button_height - 10

        for i, item in enumerate(self.menu_items):
            text = self.font.render(item, True, view_cst.TEXT_COLOR)
            rect = text.get_rect(center=((i + 0.5) * button_width, button_y))
            self.buttons.append((text, rect))

    def display(self):
        for text, rect in self.buttons:
            self.screen.blit(text, rect)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for text, rect in self.buttons:
                if rect.collidepoint(event.pos):
                    # Handle menu item click event
                    menu_item_clicked = self.menu_items[self.buttons.index((text, rect))]
                    if menu_item_clicked == "Quests":
                        return view_cst.QUEST_MENU
                    elif menu_item_clicked == "Inventory":
                        return view_cst.INVENTORY_MENU
                    elif menu_item_clicked == "Map":
                        return view_cst.MAP_MENU
