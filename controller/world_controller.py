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
        # self.view.load_entities()
        # self.view.load_entities_dict()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(view_cst.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.view.back_button_rect.collidepoint(event.pos):
                        self.world_map.set_player_coords(self.character_global_pos_x, self.character_global_pos_y)
                        return
                    else:
                        #TODO: internal workflows and window transitions may be handled in an abstract and generalized way
                        #TODO: may be better to handle events somewhere else than in the view
                        self.view.handle_dialogue_events(event)
                        self.view.handle_popup_events(event)
                        self.handle_npc_interaction(event.pos, event.button)
                    pass

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

    def handle_npc_interaction(self, pos, button):
        for npc, npc_image, npc_rect in self.view.npcs:
            if npc_rect.collidepoint(pos):
                if button == pygame.BUTTON_RIGHT:
                    # Right-click on NPC, show popup
                    print("Right-clicked on NPC")
                    self.view.create_npc_info_box(npc, npc_rect)
                    self.view.show_popup = True
                elif button == pygame.BUTTON_LEFT:
                    self.view.create_dialogue_box(npc, npc_rect)
                    self.view.show_dialogue = True
                    # Left-click on NPC, perform other actions
                    print(f"Interacting with NPC: {npc.name}")
