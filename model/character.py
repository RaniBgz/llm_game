""" Defines the character class that is used to define """
from model.entity import Entity

class Character(Entity):
    def __init__(self, hp):
        super().__init__()
        self.hp = hp
        self.inventory = []
        self.quests = []


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