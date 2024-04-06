""" Defines the character class that is used to define """
from model.entity import Entity
import json
from model.quest.quest import Quest
from model.item import Item


class Character(Entity):
    def __init__(self, name, hp, global_position=(0, 0), local_position=(0, 0), sprite="./assets/sprites/character/character.png"):
        super().__init__()
        self.name = name
        self.hp = hp
        self.sprite = sprite
        self.inventory = []
        self.quests = []
        self.global_position = global_position
        self.local_position = local_position

    def check_character_has_quest(self, quest_id):
        for quest in self.quests:
            if quest.get_id() == quest_id:
                return True
        return False

    def get_quest_by_id(self, quest_id):
        for quest in self.quests:
            if quest.get_id() == quest_id:
                return quest
        return None

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
