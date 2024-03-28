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
        self.local_map = WorldMap.get_instance().get_local_map_at(global_position[0], global_position[1])
        self.entities = self.local_map.entities
        self.npcs = []

        self.back_button_text = pygame.font.SysFont("Arial", 20).render("Back", True, view_cst.TEXT_COLOR)
        self.back_button_rect = self.back_button_text.get_rect(topright=(view_cst.WIDTH - 10, 10))

    #Go through entities dict (grid), initialize entities and add them to the entities list
    def initialize_local_map(self, x, y):
        self.local_map = WorldMap.get_instance().get_local_map_at(x, y)
        self.entities = self.local_map.entities

    def initialize_character_position(self, character):
        self.character_image = pygame.image.load(character.sprite).convert_alpha()
        self.character_image = pygame.transform.scale(self.character_image, (view_cst.TILE_WIDTH, view_cst.TILE_HEIGHT))
        # self.character_imager = pygame.transform.scale(player_image, (tile_width, tile_height))
        self.character_rect = self.character_image.get_rect(center=view_cst.SPAWN_POSITIONS_DICT["middle"])

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
                self.npcs.append((npc_image, npc_rect))

    def display_world(self, x, y):
        self.screen.fill(view_cst.WHITE)
        self.local_map = WorldMap.get_instance().get_local_map_at(x, y)
        self.screen.blit(self.character_image, self.character_rect)
        for i in range(len(self.npcs)):
            self.screen.blit(self.npcs[i][0], self.npcs[i][1])

        # self.screen.blit(self.goblin_image, self.goblin_rect)
        # for i in range(len(self.entities)):
        #     self.screen.blit(self.entities[i][0], self.entities[i][1])
        self.screen.blit(self.back_button_text, self.back_button_rect)
        self.display_coordinates(x, y)
        pygame.display.flip()




    def display_coordinates(self, x, y):
        self.coord_text = pygame.font.SysFont("Arial", 20).render(f"({x}, {y})", True, view_cst.TEXT_COLOR)
        self.coord_rect = self.coord_text.get_rect(topleft=(0, 10))
        # coord_rect.bottomleft = (10, view_cst.HEIGHT - 10)  # Position at bottom-left
        self.screen.blit(self.coord_text, self.coord_rect)