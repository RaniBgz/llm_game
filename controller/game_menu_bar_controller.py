import pygame
from view import view_constants as view_cst
from controller import controller_constants as ctrl_cst

class GameMenuBarController():
    def __init__(self, view):
        self.view = view
        self.menu_items_flags = {
            "Quests": False,
            "Inventory": False,
            "Map": False,
            "Settings": False
        }

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down_event(event)
        if event.type == pygame.MOUSEBUTTONUP:
            return_code = self.handle_mouse_up_event(event)
            if return_code:
                return return_code

    def handle_mouse_down_event(self, event):
        for i, (button_surface, button_rect, text, text_rect, button_click_color) in enumerate(self.view.buttons):
            if button_rect.collidepoint(event.pos):
                button_surface.fill(button_click_color)
                pygame.draw.rect(button_surface, view_cst.DARK_GRAY_2, button_surface.get_rect(), 2)
                self.view.buttons[i] = (button_surface, button_rect, text, text_rect, button_click_color)
                # Handle menu item click event
                menu_item_clicked = self.view.menu_items[
                    self.view.buttons.index((button_surface, button_rect, text, text_rect, button_click_color))]
                if menu_item_clicked == "Quests":
                    self.menu_items_flags["Quests"] = True
                if menu_item_clicked == "Inventory":
                    self.menu_items_flags["Inventory"] = True
                if menu_item_clicked == "Map":
                    self.menu_items_flags["Map"] = True
                if menu_item_clicked == "Settings":
                    self.menu_items_flags["Settings"] = True

    def handle_mouse_up_event(self, event):
        for i, (button_surface, button_rect, text, text_rect, button_color) in enumerate(self.view.buttons):
            if button_rect.collidepoint(event.pos):
                button_surface.fill(view_cst.DARK_GRAY)
                pygame.draw.rect(button_surface, view_cst.DARK_GRAY_2, button_surface.get_rect(), 2)
                self.view.buttons[i] = (button_surface, button_rect, text, text_rect, button_color)

                # Handle menu item click event
                menu_item_clicked = self.view.menu_items[
                    self.view.buttons.index((button_surface, button_rect, text, text_rect, button_color))]
                if menu_item_clicked == "Quests":
                    if self.menu_items_flags["Quests"]:
                        self.menu_items_flags["Quests"] = False
                        return view_cst.QUEST_MENU
                if menu_item_clicked == "Inventory":
                    if self.menu_items_flags["Inventory"]:
                        self.menu_items_flags["Inventory"] = False
                        return view_cst.INVENTORY_MENU
                if menu_item_clicked == "Map":
                    if self.menu_items_flags["Map"]:
                        self.menu_items_flags["Map"] = False
                        return view_cst.MAP_MENU
                if menu_item_clicked == "Settings":
                    if self.menu_items_flags["Settings"]:
                        self.menu_items_flags["Settings"] = False
                        return view_cst.SETTINGS_MENU

                for flag in self.menu_items_flags:
                    self.menu_items_flags[flag] = False