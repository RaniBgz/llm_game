import sys
import pygame, random
from view import view_constants as view_cst
from model.maps.world_map import WorldMap
import model.character
import model.npc

#TODO: Init character, init all entities of local map in a different function.
class WorldView:
    def __init__(self, screen, global_position):
        self.screen = screen
        # self.local_map = WorldMap.get_instance().get_local_map_at(global_position[0], global_position[1])
        # self.entities = self.local_map.entities
        self.npcs = []
        self.initialize_local_map(global_position[0], global_position[1])
        self.back_button_text = pygame.font.SysFont("Arial", 20).render("Back", True, view_cst.TEXT_COLOR)
        self.back_button_rect = self.back_button_text.get_rect(topright=(view_cst.WIDTH - 10, 10))

        self.popup_surface = None
        self.popup_rect = None
        self.popup_text = None
        self.show_popup = False

    def create_popup(self, npc, npc_rect):
        # Create a new surface for the popup window
        #TODO: see how to dynamically adjust the size of the popup window
        popup_width, popup_height = 200, 100
        self.popup_surface = pygame.Surface((popup_width, popup_height))
        self.popup_surface.fill(view_cst.POPUP_BG_COLOR)

        # Add text information about the NPC
        text = f"Name: {npc.name}"
        self.popup_text = pygame.font.SysFont("Arial", 16).render(text, True, view_cst.TEXT_COLOR)
        self.popup_surface.blit(self.popup_text, (10, 10))  # Blit the text at (10, 10) on the popup surface

        # Add a close button
        close_button_text = pygame.font.SysFont("Arial", 16).render("X", True, view_cst.TEXT_COLOR)
        close_button_rect = close_button_text.get_rect(topright=(popup_width - 10, 10))
        pygame.draw.rect(self.popup_surface, view_cst.TEXT_COLOR, close_button_rect)
        self.popup_surface.blit(close_button_text, close_button_rect)

        # Position the popup window next to the NPC
        # self.popup_rect = self.popup_surface.get_rect(center=(view_cst.WIDTH//2, view_cst.HEIGHT//2))
        self.popup_rect = self.popup_surface.get_rect(midleft=(npc_rect.midright[0] + 10, npc_rect.midright[1]))

    def display_popup(self):
        if self.show_popup:
            print(f"Displaying popup at {self.popup_rect.topleft}")
            self.screen.blit(self.popup_surface, self.popup_rect)

    def handle_popup_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the close button was clicked
            if self.popup_rect and self.popup_rect.collidepoint(event.pos):
                close_button_rect = pygame.Rect(self.popup_rect.topright[0] - 20, self.popup_rect.topright[1], 20, 20)
                if close_button_rect.collidepoint(event.pos):
                    self.show_popup = False

    #Go through entities dict (grid), initialize entities and add them to the entities list
    def initialize_local_map(self, x, y):
        self.local_map = WorldMap.get_instance().get_local_map_at(x, y)
        self.entities = self.local_map.entities
        self.npcs = []  # Clear the NPC list to start fresh
        # self.load_entities()

    def initialize_character_position(self, character):
        self.character_image = pygame.image.load(character.sprite).convert_alpha()
        self.character_image = pygame.transform.scale(self.character_image, (view_cst.TILE_WIDTH, view_cst.TILE_HEIGHT))
        # self.character_imager = pygame.transform.scale(player_image, (tile_width, tile_height))
        # self.character_rect = self.character_image.get_rect(center=view_cst.SPAWN_POSITIONS_DICT["middle"])
        self.character_rect = self.character_image.get_rect(center=(character.local_position[0]*view_cst.TILE_WIDTH-(view_cst.TILE_WIDTH/2),
                                                                  character.local_position[1]*view_cst.TILE_HEIGHT-(view_cst.TILE_HEIGHT/2)))

    def load_entities(self):
        for entity in self.entities:
            if isinstance(entity, model.character.Character):
                print(f"Loading Character: {entity.name} at {entity.local_position}")
                self.character = entity
                self.initialize_character_position(self.character)
            if isinstance(entity, model.npc.NPC):
                print(f"Loading NPC: {entity.name} at {entity.local_position}")
                npc_image = pygame.image.load(entity.sprite).convert_alpha()
                npc_image = pygame.transform.scale(npc_image, (view_cst.TILE_WIDTH, view_cst.TILE_HEIGHT))
                npc_rect = npc_image.get_rect(center=(entity.local_position[0]*view_cst.TILE_WIDTH-(view_cst.TILE_WIDTH/2),
                                                      entity.local_position[1]*view_cst.TILE_HEIGHT-(view_cst.TILE_HEIGHT/2)))
                self.npcs.append((entity, npc_image, npc_rect))

    def clear_npcs(self):
        self.npcs = []

    def display_world(self, x, y):
        self.screen.fill(view_cst.WHITE)
        self.local_map = WorldMap.get_instance().get_local_map_at(x, y)
        self.screen.blit(self.character_image, self.character_rect)
        for i in range(len(self.npcs)):
            self.screen.blit(self.npcs[i][1], self.npcs[i][2])
        self.screen.blit(self.back_button_text, self.back_button_rect)
        self.display_coordinates(x, y)
        # Blit the pop-up surface after rendering all other elements
        if self.show_popup:
            self.screen.blit(self.popup_surface, self.popup_rect)
        pygame.display.flip()

    def display_coordinates(self, x, y):
        self.coord_text = pygame.font.SysFont("Arial", 20).render(f"({x}, {y})", True, view_cst.TEXT_COLOR)
        self.coord_rect = self.coord_text.get_rect(topleft=(0, 10))
        # coord_rect.bottomleft = (10, view_cst.HEIGHT - 10)  # Position at bottom-left
        self.screen.blit(self.coord_text, self.coord_rect)