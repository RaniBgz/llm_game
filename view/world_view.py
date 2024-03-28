import sys
import pygame, random
from view import view_constants as view_cst
from model.maps.world_map import WorldMap

#TODO: Init character, init all entities of local map in a different function.
class WorldView:
    def __init__(self, screen, global_position):
        self.screen = screen
        self.local_map = WorldMap.get_instance().get_local_map_at(global_position[0], global_position[1])
        self.back_button_text = pygame.font.SysFont("Arial", 20).render("Back", True, view_cst.TEXT_COLOR)
        self.back_button_rect = self.back_button_text.get_rect(topright=(view_cst.WIDTH - 10, 10))
        self.entities = self.local_map.entities
        self.entities_dict = self.local_map.entities_dict

    #Go through entities dict (grid), initialize entities and add them to the entities list
    def initialize_local_map(self, x, y):
        self.local_map = WorldMap.get_instance().get_local_map_at(x, y)
        self.entities = self.local_map.entities

    def initialize_character_position(self, character):
        self.character_image = pygame.image.load(character.sprite).convert_alpha()
        self.character_image = pygame.transform.scale(self.character_image, (view_cst.TILE_WIDTH, view_cst.TILE_HEIGHT))
        # self.character_imager = pygame.transform.scale(player_image, (tile_width, tile_height))
        self.character_rect = self.character_image.get_rect(center=view_cst.SPAWN_POSITIONS_DICT["middle"])

    def load_entities(self, entities):
        for entity in entities:
            if ("Character" in str(type(entity))):
                self.character = entity
                self.initialize_character_position(self.character)
            else:
                entity_image = pygame.image.load(entity.sprite).convert_alpha()
                entity_image = pygame.transform.scale(entity_image, (view_cst.TILE_WIDTH, view_cst.TILE_HEIGHT))
                spawn_random = random.choice(view_cst.SPAWN_POSITIONS)
                entity_rect = entity_image.get_rect(center=spawn_random)

                # entity_rect = entity.image.get_rect(center=(view_cst.WIDTH/2,view_cst.HEIGHT/2))
                self.entities.append((entity_image, entity_rect))
                self.screen.blit(entity_image, entity_rect)

    def load_entities_dict(self):
        for (x, y), entity in self.entities_dict.items():
            print(f"x: {x}, y: {y}")
            if entity is not None:
                print(f"Entity: {entity}")
            else:
                print("Entity: None")
    def display_world(self, x, y):
        self.screen.fill(view_cst.WHITE)
        self.local_map = WorldMap.get_instance().get_local_map_at(x, y)
        # print(f"Nb Entities in local map: {len(self.local_map.entities)}")
        self.screen.blit(self.character_image, self.character_rect)
        # self.screen.blit(self.goblin_image, self.goblin_rect)
        for i in range(len(self.entities)):
            self.screen.blit(self.entities[i][0], self.entities[i][1])
        self.screen.blit(self.back_button_text, self.back_button_rect)
        self.display_coordinates(x, y)
        pygame.display.flip()




    def display_coordinates(self, x, y):
        self.coord_text = pygame.font.SysFont("Arial", 20).render(f"({x}, {y})", True, view_cst.TEXT_COLOR)
        self.coord_rect = self.coord_text.get_rect(topleft=(0, 10))
        # coord_rect.bottomleft = (10, view_cst.HEIGHT - 10)  # Position at bottom-left
        self.screen.blit(self.coord_text, self.coord_rect)