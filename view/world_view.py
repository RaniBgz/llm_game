import sys
import pygame, random
from view import view_constants as view_cst
from model.map.world_map import WorldMap
import model.character
import model.npc
import model.item
from view.ui.npc_info_box import NPCInfoBox
from view.ui.dialogue_box import DialogueBox
from view.ui.robot_dialogue_box import RobotDialogueBox
from view.ui.item_info_box import ItemInfoBox
from view.ui.game_menu_bar import GameMenuBar
from controller.game_menu_bar_controller import GameMenuBarController
from view.main_game_view import MainGameView
from controller.dialogue_controller import DialogueController
from model.observer.observer import Observer

#TODO: Init character, init all entities of local map in a different function.
class WorldView(Observer):
    def __init__(self, screen, global_position):
        Observer.__init__(self)
        self.screen = screen
        self.npcs = []
        self.items = []

        # self.observer = Observer()

        self.npc_info_box = NPCInfoBox(screen)
        self.dialogue_box = DialogueBox(screen)
        self.robot_dialogue_box = RobotDialogueBox(screen)
        self.item_info_box = ItemInfoBox(screen)

        self.character_rect = None

        # self.exit_font = pygame.font.SysFont("Arial", 30)
        # self.back_button_text = self.exit_font.render("Back", True, view_cst.TEXT_COLOR)
        # self.back_button_rect = self.back_button_text.get_rect(topright=(view_cst.WIDTH - 10, 10))

        self.initialize_local_map(global_position[0], global_position[1])

        self.game_menu_bar = GameMenuBar(screen, pygame.font.SysFont("Arial", 25))
        self.game_menu_bar_controller = GameMenuBarController(self.game_menu_bar)


    #TODO: The "kill" is currently still handled by the controller and back to the worldview. Need to refactor this to be handled by the observer/subject pattern.
    def update(self, entity, *args, **kwargs):
        if isinstance(entity, model.npc.NPC):
            if args[1] == "npc_dead":
                self.kill_npc(entity)
            elif args[1] == "npc_respawned":
                self.respawn_npc(entity)
        if isinstance(entity, model.item.Item):
            if args[1] == "item_removed_from_world":
                self.remove_item(entity)
            elif args[1] == "item_added_to_world":
                self.initialize_item(entity)


    def update_character_position(self, x, y):
        x = x * view_cst.TILE_WIDTH
        y = y * view_cst.TILE_HEIGHT
        self.character_rect.move_ip(x, y)

    def initialize_local_map(self, x, y):
        print(f"Initializing local map at {x}, {y}")
        self.local_map = WorldMap.get_instance().get_local_map_at(x, y)
        self.entities = self.local_map.entities
        self.npcs = []  # Clear the NPC list to start fresh
        self.items = []
        self.load_entities()

    def load_entities(self):
        print(f"Loading entities")
        for entity in self.entities:
            if isinstance(entity, model.character.Character):
                self.initialize_character(entity)
            if isinstance(entity, model.npc.NPC):
                entity.attach(self)
                if entity.dead:
                    continue
                else:
                    self.initialize_npc(entity)
            if isinstance(entity, model.item.Item):
                entity.attach(self)
                if entity.in_world:
                    self.initialize_item(entity)

    def initialize_character(self, character):
        print(f"Loading Character: {character.name} at {character.local_position}")
        self.character_image = pygame.image.load(character.sprite).convert_alpha()
        self.character_image = pygame.transform.scale(self.character_image, (view_cst.TILE_WIDTH, view_cst.TILE_HEIGHT))
        self.character_rect = self.character_image.get_rect(center=(
            character.local_position[0] * view_cst.TILE_WIDTH - (view_cst.TILE_WIDTH / 2),
            character.local_position[1] * view_cst.TILE_HEIGHT - (view_cst.TILE_HEIGHT / 2)))

    def initialize_item(self, item):
        print(f"Loading Item: {item.name} at {item.local_position}")
        item_image = pygame.image.load(item.sprite).convert_alpha()
        item_image = pygame.transform.scale(item_image, (view_cst.TILE_WIDTH, view_cst.TILE_HEIGHT//2))
        item_rect = item_image.get_rect(center=(
            item.local_position[0] * view_cst.TILE_WIDTH - (view_cst.TILE_WIDTH / 2),
            item.local_position[1] * view_cst.TILE_HEIGHT - (view_cst.TILE_HEIGHT / 2)))
        self.items.append((item, item_image, item_rect))

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
        self.npc_info_box.create_npc_info(npc, npc_rect)
        self.npc_info_box.show = True


    def create_dialogue_box(self, npc, character, dialogue, dialogue_type):
        print(f"Creating dialogue box for {npc.name}")
        self.dialogue_controller = DialogueController(
            self.screen, self.dialogue_box, npc, character, dialogue, dialogue_type)

        self.dialogue_controller.start_dialogue()
        # self.dialogue_box.create_dialogue(npc, dialogue_text)
        self.dialogue_box.show = True



    def create_item_info_box(self, item, item_rect):
        print(f"Creating item info box for {item.name}")
        self.item_info_box.create_item_info(item, item_rect)
        self.item_info_box.show = True

    def reset_dialogue(self):
        self.dialogue_box.show = False

    def reset_npc_popup(self):
        self.npc_info_box.show = False

    def reset_item_popup(self):
        self.item_info_box.show = False

    def handle_popup_events(self, event):
        if self.npc_info_box.show:
            self.npc_info_box.handle_events(event)
        if self.item_info_box.show:
            self.item_info_box.handle_events(event)

    def handle_dialogue_events(self, event):
        print(f"Handling dialogue events")
        if self.dialogue_box.show:
            print(f"Dialogue box is showing")
            return_code = self.dialogue_controller.handle_events(event)
            return return_code

    def handle_game_menu_events(self, event):
        return_code = self.game_menu_bar_controller.handle_events(event)
        print("Return code: ", return_code)
        return return_code

    def kill_npc(self, npc):
        for i, (npc_obj, npc_image, npc_rect) in enumerate(self.npcs):
            if npc_obj == npc:
                self.npcs.pop(i)
                npc_obj.kill()
                break

    def respawn_npc(self, npc):
        print(f"In respawn NPC")
        self.initialize_npc(npc)

    def remove_item(self, item):
        print(f"Removing item {item.name} from world")
        print(f"Length of items in world: {len(self.items)}")
        for i, (item_obj, item_image, item_rect) in enumerate(self.items):
            if item_obj.get_id() == item.get_id():
                self.items.pop(i)
                item_obj.in_world = False
                break

    def render_background(self):
        self.screen.fill(view_cst.WHITE)


    def render_character(self):
        self.screen.blit(self.character_image, self.character_rect)

    def render_npcs(self):
        for i in range(len(self.npcs)):
            self.screen.blit(self.npcs[i][1], self.npcs[i][2])

    def render_npc(self, npc, npc_image, npc_rect):
        self.screen.blit(self.npc_image, self.npc_rect)

    def render_items(self):
        for i in range(len(self.items)):
            self.screen.blit(self.items[i][1], self.items[i][2])

    def render_coordinates(self, x, y):
        self.coord_text = pygame.font.SysFont("Arial", 20).render(f"({x}, {y})", True, view_cst.TEXT_COLOR)
        self.coord_rect = self.coord_text.get_rect(topleft=(0, 10))
        self.screen.blit(self.coord_text, self.coord_rect)

    #TODO: Add render functions
    #TODO: Think about subcontrollers to handle the logic in parts of the view: killing npcs, removing items, then later health bars, etc.

    def render(self, x, y):
        self.render_background()
        self.render_npcs()
        self.render_character()
        self.render_items()
        self.render_coordinates(x, y)
        self.game_menu_bar.display()
        self.dialogue_box.display()
        self.item_info_box.display()
        self.npc_info_box.display()
        pygame.display.flip()


