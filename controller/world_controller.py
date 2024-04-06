import sys
import pygame

import model.quest.objective
from model.map.world_map import WorldMap
from model.dialogue_manager import DialogueManager
from model.quest.quest_manager import QuestManager
from view import view_constants as view_cst
from view.quest_view import QuestView
from view.inventory_view import InventoryView
from view.map_view import MapView
from view.settings_view import SettingsView
from controller.quest_controller import QuestController
from controller.inventory_controller import InventoryController
from controller.map_controller import MapController
from controller.settings_controller import SettingsController


class WorldController:
    def __init__(self, game_data, view):
        self.game_data = game_data
        self.view = view
        self.world_map = WorldMap.get_instance()
        self.local_map = self.world_map.get_local_map_at(self.game_data.character.global_position[0],
                                                         self.game_data.character.global_position[1])
        self.quest_manager = QuestManager(self.game_data)

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

                        dialogue_return_code = self.view.handle_dialogue_events(event)
                        self.handle_dialogue_return(dialogue_return_code)

                        menu_return_code = self.view.handle_game_menu_events(event)
                        self.open_menu(menu_return_code)

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

    def handle_dialogue_return(self, return_code):
        if return_code == "accept_quest":
            print("Accepting quest")
            self.quest_manager.give_quest_to_character(self.quest_manager.current_quest)
        elif return_code == "decline_quest":
            print("Declining quest")
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
            self.quest_manager.check_location_objective_completion()
        self.local_map = self.world_map.get_local_map_at(self.game_data.character.global_position[0], self.game_data.character.global_position[1])
        self.view.local_map = self.local_map
        self.view.display_world(self.game_data.character.global_position[0], self.game_data.character.global_position[1])

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
                        self.quest_manager.check_kill_objective_completion(npc)

                    else:
                        #TODO: Keep refining dialogue system
                        print(f"Interacting with NPC: {npc.name}")
                        self.quest_manager.check_talk_to_npc_objective_completion(npc)
                        self.view.show_dialogue = True
                        quest = self.quest_manager.get_random_npc_quest(npc)
                        dialogue_manager = DialogueManager(npc, self.game_data.character, quest)
                        #TODO: In the future, a higher structure will give the right quest to the Dialogue Manager
                        dialogue, dialogue_type = dialogue_manager.get_dialogue()
                        self.view.create_dialogue_box(npc, self.game_data.character, dialogue, dialogue_type)


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
                    self.quest_manager.check_retrieval_objective_completion(item)