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
        clock = pygame.time.Clock()
        moving_left = moving_right = moving_up = moving_down = False

        while True:
            clock.tick(view_cst.FPS)  # Limit the frame rate
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        moving_left = True
                    elif event.key == pygame.K_RIGHT:
                        moving_right = True
                    elif event.key == pygame.K_UP:
                        moving_up = True
                    elif event.key == pygame.K_DOWN:
                        moving_down = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        moving_left = False
                    elif event.key == pygame.K_RIGHT:
                        moving_right = False
                    elif event.key == pygame.K_UP:
                        moving_up = False
                    elif event.key == pygame.K_DOWN:
                        moving_down = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.view.back_button_rect.collidepoint(event.pos):
                        self.world_map.set_player_coords(self.character_global_pos_x, self.character_global_pos_y)
                        return

            keys_pressed = pygame.key.get_pressed()
            self.move_character(keys_pressed)
            self.view.display_world(self.character_global_pos_x, self.character_global_pos_y)

    def move_character(self, keys_pressed):
        x_change = y_change = 0
        speed = view_cst.TILE_WIDTH // view_cst.MOVEMENT_SPEED  # Calculate speed based on desired tiles per second

        if keys_pressed[pygame.K_LEFT]:
            x_change = -view_cst.TILE_WIDTH
        if keys_pressed[pygame.K_RIGHT]:
            x_change = view_cst.TILE_WIDTH
        if keys_pressed[pygame.K_UP]:
            y_change = -view_cst.TILE_HEIGHT
        if keys_pressed[pygame.K_DOWN]:
            y_change = view_cst.TILE_HEIGHT

        # Move the character and check boundaries
        self.view.character_rect.move_ip(x_change, y_change)
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
