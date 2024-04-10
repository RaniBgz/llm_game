import pygame
from view import view_constants as view_cst
from controller import controller_constants as ctrl_cst

class GameMenuBarController():
    def __init__(self, view):
        self.view = view

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button_surface, button_rect, text, text_rect, button_hover_color in self.view.buttons:
                if button_rect.collidepoint(event.pos):
                    # Handle menu item click event
                    menu_item_clicked = self.view.menu_items[self.view.buttons.index((button_surface, button_rect, text, text_rect, button_hover_color))]
                    self.subject.notify(menu_item_clicked)
                    # if menu_item_clicked == "Quests":
                    #     return view_cst.QUEST_MENU
                    # elif menu_item_clicked == "Inventory":
                    #     return view_cst.INVENTORY_MENU
                    # elif menu_item_clicked == "Map":
                    #     return view_cst.MAP_MENU
                    # elif menu_item_clicked == "Settings":
                    #     return view_cst.SETTINGS_MENU