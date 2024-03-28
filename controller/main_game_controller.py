import sys
import pygame
from view.inventory_view import InventoryView
from view.quest_view import QuestView
from view.map_view import MapView
from view.world_view import WorldView
from controller.inventory_controller import InventoryController
from controller.quest_controller import QuestController
from controller.map_controller import MapController
from controller.world_controller import WorldController

class MainGameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.view.inventory_rect.collidepoint(event.pos):
                        inventory_view = InventoryView(self.view.screen)
                        inventory_controller = InventoryController(self.model, inventory_view)
                        inventory_controller.run()  # Run the inventory loop
                    if self.view.quests_rect.collidepoint(event.pos):
                        quest_view = QuestView(self.view.screen)
                        quest_controller = QuestController(self.model, quest_view)
                        quest_controller.run()
                    elif self.view.map_rect.collidepoint(event.pos):
                        map_view = MapView(self.view.screen)
                        map_controller = MapController(self.model, map_view)
                        map_controller.run()
                    elif self.view.world_rect.collidepoint(event.pos):
                        world_view = WorldView(self.view.screen, self.model.character.global_position)
                        world_controller = WorldController(self.model, world_view)
                        world_controller.run()

            self.view.draw()