""" Defines the character class that is used to define """
from model.entity import Entity

class Character(Entity):
    def __init__(self, hp):
        super().__init__()
        self.hp = hp
        self.inventory = []
        self.quests = []
        self.location = None
        self.current_map = None  # Add this attribute to track the current map


    def add_item_to_inventory(self, item):
        self.inventory.append(item)

    def remove_item_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def add_quest(self, quest):
        self.quests.append(quest)

    def remove_quest(self, quest):
        if quest in self.quests:
            self.quests.remove(quest)

    def change_map(self, new_map):
        # If the new map is not None, the character is moving to a new map
        if new_map is not None:
            self.current_map = new_map
            self.location = None  # Reset the character's location on the new map