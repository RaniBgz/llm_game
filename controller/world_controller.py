import sys
import pygame
from view import view_constants as view_cst
from model.maps.world_map import WorldMap

class WorldController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.world_map = WorldMap.get_instance()
        self.character = self.model.character

        # self.character_pos_x, self.character_pos_y = self.world_map.get_player_coords()
        self.character_global_pos_x, self.character_global_pos_y = self.character.global_position

        self.local_map = self.world_map.get_local_map_at(self.character_global_pos_x, self.character_global_pos_y)
        self.entities = self.local_map.entities
        self.view.load_entities()
        # self.view.load_entities_dict()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # self.keys_pressed[event.key] = True
                    self.move_character(event.key)
                # if event.type == pygame.KEYUP:
                    # self.keys_pressed[event.key] = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.view.back_button_rect.collidepoint(event.pos):
                        self.world_map.set_player_coords(self.character_global_pos_x, self.character_global_pos_y)
                        return
            self.view.display_world(self.character_global_pos_x, self.character_global_pos_y)

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
        # self.character_pos_x, self.character_pos_y = self.view.character_rect.x, self.view.character_rect.y
        self.wrap_character()

    #TODO: when the character wraps to another local map, we need to remove it from the 0, 0 local map and add it to the new one
    def wrap_character(self):
        is_wrapped = False
        if self.view.character_rect.left < 0:
            self.view.character_rect.right = view_cst.WIDTH
            self.character_global_pos_x = self.character_global_pos_x - 1
            is_wrapped = True
        elif self.view.character_rect.right > view_cst.WIDTH:
            self.view.character_rect.left = 0
            self.character_global_pos_x = self.character_global_pos_x + 1
            is_wrapped = True
        if self.view.character_rect.top < 0:
            self.view.character_rect.bottom = view_cst.HEIGHT
            self.character_global_pos_y = self.character_global_pos_y + 1
            is_wrapped = True
        elif self.view.character_rect.bottom > view_cst.HEIGHT:
            self.view.character_rect.top = 0
            self.character_global_pos_y = self.character_global_pos_y - 1
            is_wrapped = True
            # Update coordinates in the WorldMap
        self.world_map.set_player_coords(self.character_global_pos_x, self.character_global_pos_y)

        if is_wrapped:
            print(f"Character wrapped to {self.character_global_pos_x}, {self.character_global_pos_y}! Updating local map...")
            self.view.initialize_local_map(self.character_global_pos_x, self.character_global_pos_y)
            self.view.load_entities()
        x, y = self.world_map.get_player_coords()
        self.local_map = self.world_map.get_local_map_at(self.character_global_pos_x, self.character_global_pos_y)
        self.view.local_map = self.local_map
        self.view.display_world(self.character_global_pos_x, self.character_global_pos_y)
