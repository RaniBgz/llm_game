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
        self.npcs = []

        self.popup_surface = None
        self.popup_rect = None
        self.show_popup = False

        self.dialogue_surface = None
        self.dialogue_rect = None
        self.show_dialogue = False

        self.back_button_text = pygame.font.SysFont("Arial", 20).render("Back", True, view_cst.TEXT_COLOR)
        self.back_button_rect = self.back_button_text.get_rect(topright=(view_cst.WIDTH - 10, 10))

        self.initialize_local_map(global_position[0], global_position[1])

    def initialize_local_map(self, x, y):
        print(f"Initializing local map at {x}, {y}")
        self.local_map = WorldMap.get_instance().get_local_map_at(x, y)
        self.entities = self.local_map.entities
        self.npcs = []  # Clear the NPC list to start fresh
        self.load_entities()

    def load_entities(self):
        for entity in self.entities:
            if isinstance(entity, model.character.Character):
                self.initialize_character(entity)
            if isinstance(entity, model.npc.NPC):
                self.initialize_npc(entity)

    def initialize_character(self, character):
        print(f"Loading Character: {character.name} at {character.local_position}")
        self.character_image = pygame.image.load(character.sprite).convert_alpha()
        self.character_image = pygame.transform.scale(self.character_image, (view_cst.TILE_WIDTH, view_cst.TILE_HEIGHT))
        self.character_rect = self.character_image.get_rect(center=(
            character.local_position[0] * view_cst.TILE_WIDTH - (view_cst.TILE_WIDTH / 2),
            character.local_position[1] * view_cst.TILE_HEIGHT - (view_cst.TILE_HEIGHT / 2)))

    def initialize_npc(self, npc):
        print(f"Loading NPC: {npc.name} at {npc.local_position}")
        npc_image = pygame.image.load(npc.sprite).convert_alpha()
        npc_image = pygame.transform.scale(npc_image, (view_cst.TILE_WIDTH, view_cst.TILE_HEIGHT))
        npc_rect = npc_image.get_rect(center=(
            npc.local_position[0] * view_cst.TILE_WIDTH - (view_cst.TILE_WIDTH / 2),
            npc.local_position[1] * view_cst.TILE_HEIGHT - (view_cst.TILE_HEIGHT / 2)))
        self.npcs.append((npc, npc_image, npc_rect))

    def create_dialogue_box(self, npc, npc_rect):
        dialogue_box_width, dialogue_box_height = view_cst.WIDTH - 20, view_cst.HEIGHT//4
        self.dialogue_surface = pygame.Surface((dialogue_box_width, dialogue_box_height))
        self.dialogue_surface.fill(view_cst.POPUP_BG_COLOR)

        text = "Test dialogue"
        self.dialogue_text = pygame.font.SysFont("Arial", 16).render(text, True, view_cst.TEXT_COLOR)
        self.dialogue_surface.blit(self.dialogue_text, (10, 10))

        # Add a close button
        close_button_text = pygame.font.SysFont("Arial", 16).render("X", True, view_cst.TEXT_COLOR)
        close_button_rect = close_button_text.get_rect(topright=(dialogue_box_width - 10, 10))
        pygame.draw.rect(self.dialogue_surface, view_cst.POPUP_BG_COLOR, close_button_rect, 1)
        self.dialogue_surface.blit(close_button_text, close_button_rect)

        # Position the popup window at the bottom of the screen
        self.dialogue_rect = self.dialogue_surface.get_rect(topleft=(10, 3*view_cst.HEIGHT//4-10))


    def create_npc_info_box(self, npc, npc_rect):
        #TODO: see how to dynamically adjust the size of the popup window
        popup_width, popup_height = 200, 100
        self.popup_surface = pygame.Surface((popup_width, popup_height))
        self.popup_surface.fill(view_cst.POPUP_BG_COLOR)

        # Add text information about the NPC
        npc_name = f"Name: {npc.name}"
        npc_name_text = pygame.font.SysFont("Arial", 16).render(npc_name, True, view_cst.TEXT_COLOR)
        self.popup_surface.blit(npc_name_text, (10, 10))  # Blit the text at (10, 10) on the popup surface

        npc_hp = f"HP: {npc.hp}"
        npc_hp_text = pygame.font.SysFont("Arial", 16).render(npc_hp, True, view_cst.TEXT_COLOR)
        self.popup_surface.blit(npc_hp_text, (10, 30))

        npc_hostile = "Hostile" if npc.hostile else "Friendly"
        txt_color = view_cst.RED if npc.hostile else view_cst.GREEN
        npc_hostile_text = pygame.font.SysFont("Arial", 16).render(npc_hostile, True, txt_color)
        self.popup_surface.blit(npc_hostile_text, (10, 50))

        # Add a close button
        close_button_text = pygame.font.SysFont("Arial", 16).render("X", True, view_cst.TEXT_COLOR)
        close_button_rect = close_button_text.get_rect(topright=(popup_width - 10, 10))
        pygame.draw.rect(self.popup_surface, view_cst.POPUP_BG_COLOR, close_button_rect, 1)
        self.popup_surface.blit(close_button_text, close_button_rect)

        # Position the popup window next to the NPC
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

    def handle_dialogue_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the close button was clicked
            if self.dialogue_rect and self.dialogue_rect.collidepoint(event.pos):
                close_button_rect = pygame.Rect(self.dialogue_rect.topright[0] - 20, self.dialogue_rect.topright[1], 20, 20)
                if close_button_rect.collidepoint(event.pos):
                    self.show_dialogue = False

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
        if self.show_dialogue:
            self.screen.blit(self.dialogue_surface, self.dialogue_rect)
        pygame.display.flip()

    def display_coordinates(self, x, y):
        self.coord_text = pygame.font.SysFont("Arial", 20).render(f"({x}, {y})", True, view_cst.TEXT_COLOR)
        self.coord_rect = self.coord_text.get_rect(topleft=(0, 10))
        self.screen.blit(self.coord_text, self.coord_rect)