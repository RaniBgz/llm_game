import sys
import pygame

import model.quest.objective
from model.quest.objective import KillObjective
from view import view_constants as view_cst
from model.map.world_map import WorldMap

class WorldController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.world_map = WorldMap.get_instance()
        self.local_map = self.world_map.get_local_map_at(self.model.character.global_position[0],
                                                         self.model.character.global_position[1])

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
                        self.model.character.global_position = (self.model.character.global_position[0],
                                                                self.model.character.global_position[1])
                        return
                    else:
                        self.view.handle_events(event)
                        self.handle_npc_interaction(event.pos, event.button)
                    pass

            keys_pressed = pygame.key.get_pressed()

            self.move_character(keys_pressed)
            self.view.display_world(self.model.character.global_position[0],
                                    self.model.character.global_position[1])

    def move_character(self, keys_pressed):
        x_change = y_change = 0

        if keys_pressed[pygame.K_LEFT]:
            x_change = -view_cst.TILE_WIDTH
            self.model.character.local_position = (self.model.character.local_position[0] - 1,
                                                   self.model.character.local_position[1])
        if keys_pressed[pygame.K_RIGHT]:
            x_change = view_cst.TILE_WIDTH
            self.model.character.local_position = (self.model.character.local_position[0] + 1,
                                                   self.model.character.local_position[1])
        if keys_pressed[pygame.K_UP]:
            y_change = -view_cst.TILE_HEIGHT
            self.model.character.local_position = (self.model.character.local_position[0],
                                                   self.model.character.local_position[1] - 1)
        if keys_pressed[pygame.K_DOWN]:
            y_change = view_cst.TILE_HEIGHT
            self.model.character.local_position = (self.model.character.local_position[0],
                                                    self.model.character.local_position[1] + 1)

        self.view.character_rect.move_ip(x_change, y_change)
        self.wrap_character()

    def wrap_character(self):
        is_wrapped = False
        if self.view.character_rect.left < 0:
            self.view.character_rect.right = view_cst.WIDTH
            self.model.character.global_position = (self.model.character.global_position[0] - 1, self.model.character.global_position[1])
            self.model.character.local_position = (view_cst.H_TILES - 1, self.model.character.local_position[1])
            is_wrapped = True
        elif self.view.character_rect.right > view_cst.WIDTH:
            self.view.character_rect.left = 0
            self.model.character.global_position = (self.model.character.global_position[0] + 1, self.model.character.global_position[1])
            self.model.character.local_position = (0, self.model.character.local_position[1])
            is_wrapped = True
        elif self.view.character_rect.top < 0:
            self.view.character_rect.bottom = view_cst.HEIGHT
            self.model.character.global_position = (self.model.character.global_position[0], self.model.character.global_position[1] + 1)
            self.model.character.local_position = (self.model.character.local_position[0], view_cst.V_TILES - 1)
            is_wrapped = True
        elif self.view.character_rect.bottom > view_cst.HEIGHT:
            self.view.character_rect.top = 0
            self.model.character.global_position = (self.model.character.global_position[0], self.model.character.global_position[1] - 1)
            self.model.character.local_position = (self.model.character.local_position[0], 0)
            is_wrapped = True
        '''Changing local map'''
        if is_wrapped:
            #TODO: Check here if the character is visiting an objective location
            self.view.reset_popup()
            self.view.reset_dialogue()
            print(f"Character wrapped to {self.model.character.global_position[0]}, {self.model.character.global_position[1]}. Updating local map...")
            self.world_map.add_entity(self.model.character, self.model.character.global_position)
            self.view.initialize_local_map(self.model.character.global_position[0], self.model.character.global_position[1])
            self.view.load_entities()
            self.check_location_objective_completion()
        self.local_map = self.world_map.get_local_map_at(self.model.character.global_position[0], self.model.character.global_position[1])
        self.view.local_map = self.local_map
        self.view.display_world(self.model.character.global_position[0], self.model.character.global_position[1])

    def check_location_objective_completion(self):
        for quest in self.model.character.quests:
            for objective in quest.objectives:
                if isinstance(objective, model.quest.objective.LocationObjective):
                    if objective.target_location == self.model.character.global_position:
                        print(f"Objective {objective.id} for quest {quest.id} is now complete")
                        quest.objectives.remove(objective)
                        if len(quest.objectives) == 0:
                            quest.completed = True
                            quest.active = False
                            print(f"Quest {quest.id} is now complete")

    def check_kill_objective_completion(self, npc):
        for quest in self.model.character.quests:
            for objective in quest.objectives:
                if isinstance(objective, model.quest.objective.KillObjective):
                    if objective.target_id == npc.id:
                        print(f"Objective {objective.id} for quest {quest.id} is now complete")
                        quest.objectives.remove(objective)
                        if len(quest.objectives) == 0:
                            quest.completed = True
                            quest.active = False
                            print(f"Quest {quest.id} is now complete")

    def check_talk_to_npc_objective_completion(self, npc):
        for quest in self.model.character.quests:
            for objective in quest.objectives:
                if isinstance(objective, model.quest.objective.TalkToNPCObjective):
                    if objective.target_npc_id == npc.id:
                        print(f"Objective {objective.id} for quest {quest.id} is now complete")
                        quest.objectives.remove(objective)
                        if len(quest.objectives) == 0:
                            quest.completed = True
                            quest.active = False
                            print(f"Quest {quest.id} is now complete")

    def handle_npc_interaction(self, pos, button):
        for npc, npc_image, npc_rect in self.view.npcs:
            if npc_rect.collidepoint(pos):
                if button == pygame.BUTTON_RIGHT:
                    # Right-click on NPC, show popup
                    print("Right-clicked on NPC")
                    self.view.show_npc_popup = True
                    self.view.create_npc_info_box(npc, npc_rect)
                elif button == pygame.BUTTON_LEFT:
                    if(npc.hostile):
                        print("Left-clicked on hostile NPC")
                        self.view.kill_npc(npc)
                        self.check_kill_objective_completion(npc)

                    else:
                        print(f"Interacting with NPC: {npc.name}")
                        self.view.show_dialogue = True
                        self.view.create_dialogue_box(npc, "test dialogue")
                        self.check_talk_to_npc_objective_completion(npc)



