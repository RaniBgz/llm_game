import sys
import pygame
import asyncio

from model.map.world_map import WorldMap
from model.dialogue.dialogue_manager import DialogueManager
from model.quest.quest_manager import QuestManager
from model.quest.quest_builder import QuestBuilder
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
    def __init__(self, game_data, main_menu_ctrl, view):
        self.game_data = game_data
        self.view = view
        self.main_menu_controller = main_menu_ctrl
        self.quest_manager = QuestManager(self.game_data)
        self.quest_builder = QuestBuilder(self.game_data)
        self.world_map = WorldMap.get_instance()
        self.local_map = self.world_map.get_local_map_at(self.game_data.character.global_position[0],
                                                         self.game_data.character.global_position[1])
        # self.movement_speed = 3 # tiles per second
        # self.time_to_move_one_tile = view_cst.FPS / self.movement_speed
        self.time_to_move_one_tile = 30
        self.accumulated_time = 0.0
        self.accumulated_frames = 0
        self.move_direction = (0, 0)


    async def run_async(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            clock.tick(view_cst.FPS)
            dt = clock.tick(view_cst.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_event(event)

            self.update_movement(dt)
            self.view.render(self.game_data.character.global_position[0],
                             self.game_data.character.global_position[1])

            await asyncio.sleep(0)

    def run(self):
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.run_async())
        except RuntimeError as e:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.run_async())
        finally:
            loop.close()


    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down_event(event)
        if event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up_event(event)
        if event.type == pygame.KEYDOWN:
            self.handle_key_down(event.key)
        if event.type == pygame.KEYUP:
            self.handle_key_up(event.key)

        menu_return_code = self.view.handle_game_menu_events(event)
        self.open_menu(menu_return_code)

        dialogue_return_code = self.view.handle_dialogue_events(event)
        self.handle_dialogue_return(dialogue_return_code)

    def handle_key_down(self, key):
        if key == pygame.K_ESCAPE:
            self.back_to_main_menu()
        if key == pygame.K_LEFT:
            self.move_direction = (-1, 0)
            self.game_data.character.update_direction("left")
            self.game_data.character.update_state("walking")
        elif key == pygame.K_RIGHT:
            self.move_direction = (1, 0)
            self.game_data.character.update_direction("right")
            self.game_data.character.update_state("walking")
        elif key == pygame.K_UP:
            self.move_direction = (0, -1)
            self.game_data.character.update_direction("up")
            self.game_data.character.update_state("walking")
        elif key == pygame.K_DOWN:
            self.move_direction = (0, 1)
            self.game_data.character.update_direction("down")
            self.game_data.character.update_state("walking")

    def update_movement(self, dt):
        self.accumulated_time += dt
        if self.move_direction != (0, 0):
            if self.accumulated_time >= self.time_to_move_one_tile:
                self.move_character()
                self.accumulated_time = 0.0
            self.game_data.character.update_animation()

    def move_character(self):
        keys_pressed = pygame.key.get_pressed()
        x_change = y_change = 0

        if keys_pressed[pygame.K_LEFT]:
            x_change = -1
        if keys_pressed[pygame.K_RIGHT]:
            x_change = 1
        if keys_pressed[pygame.K_UP]:
            y_change = -1
        if keys_pressed[pygame.K_DOWN]:
            y_change = 1

        self.game_data.character.move(x_change, y_change)
        # self.view.update_character_position(x_change, y_change) #TODO: change to subject observer pattern
        self.wrap_character()

    def handle_key_up(self, key):
        if (key == pygame.K_LEFT and self.move_direction == (-1, 0)) or \
           (key == pygame.K_RIGHT and self.move_direction == (1, 0)) or \
           (key == pygame.K_UP and self.move_direction == (0, -1)) or \
           (key == pygame.K_DOWN and self.move_direction == (0, 1)):
            self.move_direction = (0, 0)
            self.game_data.character.update_state("idle")
            self.game_data.character.update_animation()


    def handle_mouse_down_event(self, event):
        pos = event.pos #click position
        button = event.button #left or right click
        for npc, npc_image, npc_rect in self.view.npcs: #Check which NPC was clicked
            if npc_rect.collidepoint(pos):
                self.handle_npc_interaction(pos, button)

        for item, item_image, item_rect in self.view.items: #Check which Item was clicked
            if item_rect.collidepoint(pos):
                self.handle_item_interaction(pos, button)

        self.view.handle_popup_events(event)


    def handle_mouse_up_event(self, event):
        pass


    def handle_dialogue_return(self, return_code):
        if return_code == "accept_quest":
            self.quest_manager.handle_quest_giving()
        elif return_code == "decline_quest":
            pass
        elif return_code == "end_quest":
            self.quest_manager.handle_quest_completion()
        elif return_code == "generate_quest":
            llm_model = self.game_data.get_llm_model()
            game_context = self.game_data.get_game_context()
            asyncio.create_task(self.process_quest_generation_with_context(llm_model, game_context))
        else:
            return

    async def process_quest_generation_with_context(self, llm_model, game_context):
        # quest, quest_dialogue = asyncio.run(self.quest_builder.generate_quest_and_dialogue(llm_model))
        quest, quest_dialogue = await self.quest_builder.generate_quest_and_dialogue_with_context(llm_model, game_context)
        self.quest_manager.add_quest_with_dialogue_to_current_npc(quest, quest_dialogue)

    async def process_quest_generation(self, llm_model):
        quest, quest_dialogue = await self.quest_builder.generate_quest_and_dialogue(llm_model)
        self.quest_manager.add_quest_with_dialogue_to_current_npc(quest, quest_dialogue)
        self.view.dialogue_controller.handle_generate_quest_button_logic()  # Update button visibility

    def handle_npc_interaction(self, pos, button):
        time = pygame.time.get_ticks()
        for npc, npc_image, npc_rect in self.view.npcs:
            if npc_rect.collidepoint(pos):
                if button == pygame.BUTTON_RIGHT:
                    # Right-click on NPC, show popup
                    self.view.show_npc_popup = True
                    self.view.create_npc_info_box(npc, npc_rect)
                elif button == pygame.BUTTON_LEFT:
                    if(npc.hostile):
                        self.view.kill_npc(npc)
                        self.quest_manager.check_kill_objective_completion(npc)

                    else:
                        #TODO: Keep refining dialogue system
                        self.quest_manager.check_talk_to_npc_objective_completion(npc)
                        quest = self.quest_manager.get_next_npc_quest(npc)
                        self.quest_manager.set_current_npc(npc)
                        # self.quest_manager.current_npc = npc
                        dialogue_manager = DialogueManager(npc, self.game_data.character, quest)
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
                    self.pickup_item(item)
                    # self.view.pickup_item(item)
                    # self.game_data.character.inventory.append(item)
                    self.quest_manager.check_retrieval_objective_completion(item)

    def pickup_item(self, item):
        self.game_data.character.add_item_to_inventory(item)
        self.world_map.remove_entity(item, item.global_position)
        self.view.remove_item(item)

    def back_to_main_menu(self):
        self.main_menu_controller.run()

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
            return_coordinates = map_controller.run()
            if return_coordinates:
                self.teleport_character(return_coordinates)
                print(f"Character teleported to {return_coordinates[0]}, {return_coordinates[1]}, biome is")
                pass
        elif return_code == view_cst.SETTINGS_MENU:
            settings_view = SettingsView(self.view.screen)
            settings_controller = SettingsController(self.game_data, settings_view)
            settings_controller.run()
        else:
            return

    def teleport_character(self, coordinates):
        self.game_data.character.global_position = coordinates
        self.view.initialize_local_map(coordinates[0], coordinates[1])
        self.local_map = self.world_map.get_local_map_at(coordinates[0], coordinates[1])
        self.view.local_map = self.local_map

    def wrap_character(self):
        is_wrapped = False
        # print(f"Character local position: {self.game_data.character.local_position}")
        if self.view.character_rect.left < 0: #Left
            print("Left")
            self.old_position = self.game_data.character.global_position
            # self.view.character_rect.right = view_cst.WIDTH
            self.game_data.character.global_position = (self.game_data.character.global_position[0] - 1, self.game_data.character.global_position[1])
            self.game_data.character.local_position = (view_cst.H_TILES, self.game_data.character.local_position[1])
            is_wrapped = True
        elif self.view.character_rect.right > view_cst.WIDTH: #Right
            print("Right")
            self.old_position = self.game_data.character.global_position
            # self.view.character_rect.left = 0
            self.game_data.character.global_position = (self.game_data.character.global_position[0] + 1, self.game_data.character.global_position[1])
            self.game_data.character.local_position = (1, self.game_data.character.local_position[1])
            is_wrapped = True
        elif self.view.character_rect.top < 0: #Up
            print("Up")
            self.old_position = self.game_data.character.global_position
            # self.view.character_rect.bottom = view_cst.HEIGHT
            self.game_data.character.global_position = (self.game_data.character.global_position[0], self.game_data.character.global_position[1] - 1)
            self.game_data.character.local_position = (self.game_data.character.local_position[0], view_cst.V_TILES - 1)
            is_wrapped = True
        elif self.view.character_rect.bottom > view_cst.HEIGHT-view_cst.MENU_BUTTON_HEIGHT: #Down
            print("Down")
            self.old_position = self.game_data.character.global_position
            # self.view.character_rect.top = 0
            self.game_data.character.global_position = (self.game_data.character.global_position[0], self.game_data.character.global_position[1] + 1)
            self.game_data.character.local_position = (self.game_data.character.local_position[0], 1)
            is_wrapped = True
        '''Changing local map'''
        if is_wrapped:
            #TODO: Check here if the character is visiting an objective location
            self.view.reset_npc_popup()
            self.view.reset_item_popup()
            self.view.reset_dialogue()
            print(f"Character wrapped to {self.game_data.character.global_position[0]}, {self.game_data.character.global_position[1]}. Updating local map...")
            self.world_map.remove_entity(self.game_data.character, self.old_position)
            self.world_map.add_entity(self.game_data.character, self.game_data.character.global_position)
            self.view.initialize_local_map(self.game_data.character.global_position[0], self.game_data.character.global_position[1])
            self.quest_manager.check_location_objective_completion()
        self.local_map = self.world_map.get_local_map_at(self.game_data.character.global_position[0], self.game_data.character.global_position[1])
        self.view.local_map = self.local_map
        # self.view.render(self.game_data.character.global_position[0], self.game_data.character.global_position[1])
