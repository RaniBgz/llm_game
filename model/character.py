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


    # def __dict__(self):
    #     data = super().__dict__()
    #     data['inventory'] = [item.__dict__() for item in self.inventory]
    #     data['quests'] = [quest.__dict__() for quest in self.quests]
    #     return data
    # def save_character(character, filename):
    #     with open(filename, 'w') as file:
    #         json.dump(character.__dict__(), file)
    #
    # def load_character(filename):
    #     with open(filename, 'r') as file:
    #         data = json.load(file)
    #         character = Character(**data)
    #         for item_data in data['inventory']:
    #             item = Item(**item_data)
    #             character.add_item_to_inventory(item)
    #         for quest_data in data['quests']:
    #             quest = Quest(**quest_data)
    #             character.add_quest(quest)
    #         return character
