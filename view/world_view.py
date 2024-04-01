import sys
import pygame, random
from view import view_constants as view_cst
from model.map.world_map import WorldMap
import model.character
import model.npc
from view.ui.npc_info_box import NPCInfoBox
from view.ui.dialogue_box import DialogueBox

#TODO: Init character, init all entities of local map in a different function.
class WorldView:
    def __init__(self, screen, global_position):
        self.screen = screen
        self.npcs = []

        self.show_npc_popup = False
        self.npc_info_box = None

        self.show_dialogue = False
        self.dialogue_box = None

        self.character_rect = None

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
        print(f"Loading entities")
        for entity in self.entities:
            if isinstance(entity, model.character.Character):
                self.initialize_character(entity)
            if isinstance(entity, model.npc.NPC):
                if entity.dead:
                    continue
                else:
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

    def create_npc_info_box(self, npc, npc_rect):
        print(f"Creating NPC info box for {npc.name}")
        self.npc_info_box = NPCInfoBox(self.screen, npc, npc_rect)
        self.npc_info_box.show = True

    def create_dialogue_box(self, npc, dialogue_text):
        print(f"Creating dialogue box for {npc.name}")
        self.dialogue_box = DialogueBox(self.screen, npc, dialogue_text)
        self.dialogue_box.show = True

    def reset_dialogue(self):
        self.show_dialogue = False

    def reset_popup(self):
        self.show_npc_popup = False


    def handle_events(self, event):
        if self.npc_info_box:
            if self.npc_info_box.handle_events(event):
                self.npc_info_box = None
                self.show_npc_popup = False

        if self.dialogue_box:
            if self.dialogue_box.handle_events(event):
                self.dialogue_box = None
                self.show_dialogue = False

    def kill_npc(self, npc):
        for i, (npc_obj, npc_image, npc_rect) in enumerate(self.npcs):
            if npc_obj == npc:
                self.npcs.pop(i)
                npc_obj.dead = True
                break

    def display_world(self, x, y):
        self.screen.fill(view_cst.WHITE)
        self.local_map = WorldMap.get_instance().get_local_map_at(x, y)
        self.screen.blit(self.character_image, self.character_rect)
        for i in range(len(self.npcs)):
            self.screen.blit(self.npcs[i][1], self.npcs[i][2])
        self.screen.blit(self.back_button_text, self.back_button_rect)
        self.display_coordinates(x, y)
        # Blit the pop-up surface after rendering all other elements
        if self.show_npc_popup:
            self.npc_info_box.display()
            print(f"Displaying NPC info box")
            # self.screen.blit(self.popup_surface, self.popup_rect)
        if self.show_dialogue:
            print(f"Displaying dialogue")
            self.dialogue_box.display()
            # self.screen.blit(self.dialogue_surface, self.dialogue_rect)
        pygame.display.flip()

    def display_coordinates(self, x, y):
        self.coord_text = pygame.font.SysFont("Arial", 20).render(f"({x}, {y})", True, view_cst.TEXT_COLOR)
        self.coord_rect = self.coord_text.get_rect(topleft=(0, 10))
        self.screen.blit(self.coord_text, self.coord_rect)