import sys
import pygame
from view import view_constants as view_cst
from model.world_map import WorldMap

class WorldController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        # self.character_pos_x = 0
        # self.character_pos_y = 0
        self.world_map = WorldMap.get_instance()
        self.character_pos_x, self.character_pos_y = self.world_map.get_player_coords()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.move_character(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.view.back_button_rect.collidepoint(event.pos):
                        return

            self.view.display_world(self.character_pos_x, self.character_pos_y)

    def move_character(self, key):
        x_change = y_change = 0
        if key == pygame.K_DOWN:
            y_change = self.view.character_image.get_height()
        elif key == pygame.K_UP:
            y_change = -self.view.character_image.get_height()
        elif key == pygame.K_LEFT:
            x_change = -self.view.character_image.get_width()
        elif key == pygame.K_RIGHT:
            x_change = self.view.character_image.get_width()

        # Move the character and check boundaries
        self.view.character_rect.move_ip(x_change, y_change)
        self.wrap_character()

    def wrap_character(self):
        character_width = self.view.character_image.get_width()
        character_height = self.view.character_image.get_height()
        if self.view.character_rect.left < 0:
            self.view.character_rect.right = view_cst.WIDTH
            self.character_pos_x = self.character_pos_x - 1
        elif self.view.character_rect.right > view_cst.WIDTH:
            self.view.character_rect.left = 0
            self.character_pos_x = self.character_pos_x + 1
        if self.view.character_rect.top < 0:
            self.view.character_rect.bottom = view_cst.HEIGHT
            self.character_pos_y = self.character_pos_y + 1
        elif self.view.character_rect.bottom > view_cst.HEIGHT:
            self.view.character_rect.top = 0
            self.character_pos_y = self.character_pos_y - 1
            # Update coordinates in the WorldMap
        self.world_map.set_player_coords(self.view.character_rect.x, self.view.character_rect.y)
        x, y = self.world_map.get_player_coords()
        self.view.display_coordinates(x, y)
