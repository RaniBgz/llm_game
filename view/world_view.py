import sys
import pygame
from view import view_constants as view_cst
from model.maps.world_map import WorldMap

#TODO: Init character, init all entities of local map in a different function.
class WorldView:
    def __init__(self, screen):
        self.screen = screen
        self.local_map = None
        # self.initialize_character_position()

        # self.character_image = pygame.image.load("assets/sprites/character.png").convert_alpha()

        self.character_image = pygame.image.load("assets/sprites/character.png").convert_alpha()
        self.character_rect = self.character_image.get_rect(center=view_cst.SPAWN_POSITIONS_DICT["middle"])

        self.goblin_image = pygame.image.load("assets/sprites/goblin.png").convert_alpha()
        self.goblin_rect = self.goblin_image.get_rect(center=view_cst.SPAWN_POSITIONS_DICT["top_right"])


        self.back_button_text = pygame.font.SysFont("Arial", 20).render("Back", True, view_cst.TEXT_COLOR)
        self.back_button_rect = self.back_button_text.get_rect(topright=(view_cst.WIDTH - 10, 10))

    def initialize_character_position(self, character):
        self.character_image = pygame.image.load(character.sprite).convert_alpha()
        self.character_rect = self.character_image.get_rect(center=view_cst.SPAWN_POSITIONS_DICT["middle"])


    def display_world(self, x, y):
        self.screen.fill(view_cst.WHITE)
        self.local_map = WorldMap.get_instance().get_local_map_at(x, y)
        # print(f"Nb Entities in local map: {len(self.local_map.entities)}")
        self.screen.blit(self.character_image, self.character_rect)
        self.screen.blit(self.goblin_image, self.goblin_rect)
        self.screen.blit(self.back_button_text, self.back_button_rect)
        self.display_coordinates(x, y)
        pygame.display.flip()

    def load_entities(self, entities):
        for entity in entities:
            entity_image = pygame.image.load(entity.sprite).convert_alpha()
            entity_rect = entity_image.get_rect(center=(view_cst.WIDTH//2, view_cst.HEIGHT//2))
            # entity_rect = entity.image.get_rect(center=(view_cst.WIDTH/2,view_cst.HEIGHT/2))
            self.screen.blit(entity.image, entity_rect)


    def display_coordinates(self, x, y):
        self.coord_text = pygame.font.SysFont("Arial", 20).render(f"({x}, {y})", True, view_cst.TEXT_COLOR)
        self.coord_rect = self.coord_text.get_rect(topleft=(0, 10))
        # coord_rect.bottomleft = (10, view_cst.HEIGHT - 10)  # Position at bottom-left
        self.screen.blit(self.coord_text, self.coord_rect)