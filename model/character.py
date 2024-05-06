""" Defines the character class that is used to define """
from model.entity import Entity
import json
from model.quest.quest import Quest
from model.item import Item
from model.subject.subject import Subject


class Character(Entity):
    def __init__(self, name,
                 hp,
                 global_position=(0, 0),
                 local_position=(0, 0),
                 sprite="./assets/sprites/character/character_idle_up.png",
                 embedding=None):
        super().__init__()
        self.name = name
        self.hp = hp
        self.sprite = sprite
        self.sprites = {
            "down": "./assets/sprites/character/character_idle_down.png",
            "up": "./assets/sprites/character/character_idle_up.png",
            "left": "./assets/sprites/character/character_idle_left.png",
            "right": "./assets/sprites/character/character_idle_right.png"
        }
        self.inventory = []
        self.quests = []
        self.global_position = global_position
        self.local_position = local_position
        self.embedding = embedding

    def attach(self, observer):
        self.subject.attach(observer)

    def detach(self, observer):
        self.subject.detach(observer)

    def take_damage(self, damage):
        self.hp -= damage
        self.subject.notify()

    def move(self, x_change, y_change):
        self.local_position = (self.local_position[0] + x_change, self.local_position[1] + y_change)
        # self.subject.notify()

    def check_character_has_quest(self, quest_id):
        for quest in self.quests:
            if quest.get_id() == quest_id:
                return True
        return False

    def has_item(self, item_id):
        for item in self.inventory:
            if item.get_id() == item_id:
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
