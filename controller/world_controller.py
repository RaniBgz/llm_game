import sys
import pygame

import model.quest.objective
from view import view_constants as view_cst
from model.map.world_map import WorldMap
from view.quest_view import QuestView
from view.inventory_view import InventoryView
from view.map_view import MapView
from view.settings_view import SettingsView
from controller.quest_controller import QuestController
from controller.inventory_controller import InventoryController
from controller.map_controller import MapController
from controller.settings_controller import SettingsController
from controller.dialogue_controller import DialogueController

class WorldController:
    def __init__(self, game_data, view):
        self.game_data = game_data
        self.view = view
        self.world_map = WorldMap.get_instance()
        self.local_map = self.world_map.get_local_map_at(self.game_data.character.global_position[0],
                                                         self.game_data.character.global_position[1])

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
                        self.game_data.character.global_position = (self.game_data.character.global_position[0],
                                                                    self.game_data.character.global_position[1])
                        return
                    else:
                        self.view.handle_popup_events(event)
                        self.view.handle_dialogue_events(event)
                        return_code = self.view.handle_game_menu_events(event)
                        self.open_menu(return_code)
                        self.handle_npc_interaction(event.pos, event.button)
                        self.handle_item_interaction(event.pos, event.button)
                    pass

            keys_pressed = pygame.key.get_pressed()
            self.move_character(keys_pressed)
            self.view.display_world(self.game_data.character.global_position[0],
                                    self.game_data.character.global_position[1])

    def open_menu(self, return_code):
        if return_code == view_cst.QUEST_MENU:
            quest_view = QuestView(self.view.screen)
            quest_controller = QuestController(self.game_data, quest_view)
            quest_controller.run()
        elif return_code == view_cst.INVENTORY_MENU:
            inventory_view = InventoryView(self.view.screen)
            inventory_controller = InventoryController(self.game_data, inventory_view)
            inventory_controller.run()  # Run the inventory loop
        elif return_code == view_cst.MAP_MENU:
            map_view = MapView(self.view.screen)
            map_controller = MapController(self.game_data, map_view)
            map_controller.run()
        elif return_code == view_cst.SETTINGS_MENU:
            settings_view = SettingsView(self.view.screen)
            settings_controller = SettingsController(self.game_data, settings_view)
            settings_controller.run()
        else:
            return

    def move_character(self, keys_pressed):
        x_change = y_change = 0

        if keys_pressed[pygame.K_LEFT]:
            x_change = -view_cst.TILE_WIDTH
            self.game_data.character.local_position = (self.game_data.character.local_position[0] - 1,
                                                       self.game_data.character.local_position[1])
        if keys_pressed[pygame.K_RIGHT]:
            x_change = view_cst.TILE_WIDTH
            self.game_data.character.local_position = (self.game_data.character.local_position[0] + 1,
                                                       self.game_data.character.local_position[1])
        if keys_pressed[pygame.K_UP]:
            y_change = -view_cst.TILE_HEIGHT
            self.game_data.character.local_position = (self.game_data.character.local_position[0],
                                                       self.game_data.character.local_position[1] - 1)
        if keys_pressed[pygame.K_DOWN]:
            y_change = view_cst.TILE_HEIGHT
            self.game_data.character.local_position = (self.game_data.character.local_position[0],
                                                       self.game_data.character.local_position[1] + 1)

        self.view.character_rect.move_ip(x_change, y_change)
        self.wrap_character()

    def wrap_character(self):
        is_wrapped = False
        # print(f"Character local position: {self.game_data.character.local_position}")
        if self.view.character_rect.left < 0:
            self.view.character_rect.right = view_cst.WIDTH
            self.game_data.character.global_position = (self.game_data.character.global_position[0] - 1, self.game_data.character.global_position[1])
            self.game_data.character.local_position = (view_cst.H_TILES - 1, self.game_data.character.local_position[1])
            is_wrapped = True
        elif self.view.character_rect.right > view_cst.WIDTH:
            self.view.character_rect.left = 0
            self.game_data.character.global_position = (self.game_data.character.global_position[0] + 1, self.game_data.character.global_position[1])
            self.game_data.character.local_position = (0, self.game_data.character.local_position[1])
            is_wrapped = True
        elif self.view.character_rect.top < 0:
            self.view.character_rect.bottom = view_cst.HEIGHT
            self.game_data.character.global_position = (self.game_data.character.global_position[0], self.game_data.character.global_position[1] + 1)
            self.game_data.character.local_position = (self.game_data.character.local_position[0], view_cst.V_TILES - 1)
            is_wrapped = True
        elif self.view.character_rect.bottom > view_cst.HEIGHT-view_cst.MENU_BUTTON_HEIGHT:
            self.view.character_rect.top = 0
            self.game_data.character.global_position = (self.game_data.character.global_position[0], self.game_data.character.global_position[1] - 1)
            self.game_data.character.local_position = (self.game_data.character.local_position[0], 0)
            is_wrapped = True
        '''Changing local map'''
        if is_wrapped:
            #TODO: Check here if the character is visiting an objective location
            self.view.reset_npc_popup()
            self.view.reset_item_popup()
            self.view.reset_dialogue()
            print(f"Character wrapped to {self.game_data.character.global_position[0]}, {self.game_data.character.global_position[1]}. Updating local map...")
            self.world_map.add_entity(self.game_data.character, self.game_data.character.global_position)
            self.view.initialize_local_map(self.game_data.character.global_position[0], self.game_data.character.global_position[1])
            self.check_location_objective_completion()
        self.local_map = self.world_map.get_local_map_at(self.game_data.character.global_position[0], self.game_data.character.global_position[1])
        self.view.local_map = self.local_map
        self.view.display_world(self.game_data.character.global_position[0], self.game_data.character.global_position[1])

    #TODO: If moving this away from the World Controller, make sure to pass the parameters needed
    def check_location_objective_completion(self):
        for quest in self.game_data.character.quests:
            if quest.ordered:
                current_objective = quest.get_current_objective()
                if isinstance(current_objective, model.quest.objective.LocationObjective):
                    if current_objective.target_location == self.game_data.character.global_position:
                        current_objective.set_completed()
                        print(f"Objective {current_objective.id} for quest {quest.id} is now complete")
                        if not quest.point_to_next_objective():
                            quest.set_inactive()
                            print(f"Quest {quest.id} is now complete")
            else:
                for objective in quest.objectives:
                    if isinstance(objective, model.quest.objective.LocationObjective):
                        if objective.target_location == self.game_data.character.global_position:
                            objective.set_completed()
                            print(f"Objective {objective.id} for quest {quest.id} is now complete")
                            if quest.check_all_objectives_completed():
                                quest.set_inactive()
                                print(f"Quest {quest.id} is now complete")


    def check_kill_objective_completion(self, npc):
        for quest in self.game_data.character.quests:
            if quest.ordered:
                current_objective = quest.get_current_objective()
                if isinstance(current_objective, model.quest.objective.KillObjective):
                    if current_objective.target_id == npc.id:
                        current_objective.set_completed()
                        print(f"Objective {current_objective.id} for quest {quest.id} is now complete")
                        if not quest.point_to_next_objective():
                            quest.set_inactive()
                            print(f"Quest {quest.id} is now complete")
            else:
                for objective in quest.objectives:
                    if isinstance(objective, model.quest.objective.KillObjective):
                        if objective.target_id == npc.id:
                            objective.set_completed()
                            print(f"Objective {objective.id} for quest {quest.id} is now complete")
                            if quest.check_all_objectives_completed():
                                quest.set_inactive()
                                print(f"Quest {quest.id} is now complete")


    def check_talk_to_npc_objective_completion(self, npc):
        for quest in self.game_data.character.quests:
            if quest.ordered:
                current_objective = quest.get_current_objective()
                if isinstance(current_objective, model.quest.objective.TalkToNPCObjective):
                    if current_objective.target_npc_id == npc.id:
                        current_objective.set_completed()
                        print(f"Objective {current_objective.id} for quest {quest.id} is now complete")
                        if not quest.point_to_next_objective():
                            quest.set_inactive()
                            print(f"Quest {quest.id} is now complete")
            else:
                for objective in quest.objectives:
                    if isinstance(objective, model.quest.objective.TalkToNPCObjective):
                        if objective.target_npc_id == npc.id:
                            objective.set_completed()
                            print(f"Objective {objective.id} for quest {quest.id} is now complete")
                            if quest.check_all_objectives_completed():
                                quest.set_inactive()
                                print(f"Quest {quest.id} is now complete")

    def check_retrieval_objective_completion(self, item):
        for quest in self.game_data.character.quests:
            if quest.ordered:
                current_objective = quest.get_current_objective()
                if isinstance(current_objective, model.quest.objective.RetrievalObjective):
                    if current_objective.target_item_id == item.id:
                        current_objective.set_completed()
                        print(f"Objective {current_objective.id} for quest {quest.id} is now complete")
                        if not quest.point_to_next_objective():
                            quest.set_inactive()
                            print(f"Quest {quest.id} is now complete")
            else:
                for objective in quest.objectives:
                    if isinstance(objective, model.quest.objective.RetrievalObjective):
                        if objective.target_item_id == item.id:
                            objective.set_completed()
                            print(f"Objective {objective.id} for quest {quest.id} is now complete")
                            if quest.check_all_objectives_completed():
                                quest.set_inactive()
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
                        self.view.create_dialogue_box(npc, self.game_data.character)
                        #TODO: Here dialoguecontroller should be initialized
                        # self.view.create_dialogue_box(npc, "test dialogue")
                        self.check_talk_to_npc_objective_completion(npc)

    def handle_item_interaction(self, pos, button):
        for item, item_image, item_rect in self.view.items:
            if item_rect.collidepoint(pos):
                if button == pygame.BUTTON_RIGHT:
                    # Right-click on Item, show popup
                    print("Right-clicked on Item")
                    self.view.show_item_popup = True
                    self.view.create_item_info_box(item, item_rect)
                elif button == pygame.BUTTON_LEFT:
                    print(f"Interacting with Item: {item.name}")
                    self.view.pickup_item(item)
                    self.game_data.character.inventory.append(item)
                    self.check_retrieval_objective_completion(item)