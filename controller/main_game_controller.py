import sys
import pygame
from view.inventory_view import InventoryView
from view.quest_view import QuestView
from controller.inventory_controller import InventoryController
from controller.quest_controller import QuestController

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
                        # ... Handle button clicks for quests, inventory, etc.

            self.view.draw()