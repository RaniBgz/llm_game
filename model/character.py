""" Defines the character class that is used to define """
from model.entity import Entity
import pygame
import view.view_constants as view_cst
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
        self.directions = ["up", "down", "left", "right"]
        self.idle_sprites = {}
        self.initialize_idle_sprites()
        # self.idle_sprites = {
        #     "down": "./assets/sprites/character/character_idle_down.png",
        #     "up": "./assets/sprites/character/character_idle_up.png",
        #     "left": "./assets/sprites/character/character_idle_left.png",
        #     "right": "./assets/sprites/character/character_idle_right.png"
        # }
        self.walking_sprites = {
            "down": [f"./assets/sprites/character/character_walk_down_{i}.png" for i in range(1, 6)],
            "up": [f"./assets/sprites/character/character_walk_up_{i}.png" for i in range(1, 6)],
            "left": [f"./assets/sprites/character/character_walk_left_{i}.png" for i in range(1, 6)],
            "right": [f"./assets/sprites/character/character_walk_right_{i}.png" for i in range(1, 6)]
        }
        self.current_sprite = self.idle_sprites["down"]
        self.inventory = []
        self.quests = []
        self.global_position = global_position
        self.local_position = local_position
        self.embedding = embedding

    def attach(self, observer):
        self.subject.attach(observer)

    def detach(self, observer):
        self.subject.detach(observer)

    def initialize_idle_sprites(self):
        for direction in self.directions:
            sprite_path = f"./assets/sprites/character/character_idle_{direction}.png"
            self.idle_sprites[direction] = pygame.image.load(sprite_path).convert_alpha()
            self.idle_sprites[direction] = pygame.transform.scale(self.idle_sprites[direction], (view_cst.TILE_WIDTH, view_cst.TILE_HEIGHT))

    def initialize_current_sprite(self):
        self.current_sprite = self.idle_sprites["down"]

    def update_direction(self, direction):
        if direction in self.directions:
            self.current_sprite = self.idle_sprites[direction]

    def set_current_sprite(self, state, direction):
        if state=="idle":
            self.current_sprite = self.idle_sprites[direction]
        elif state=="moving":
            self.current_sprite = self.walking_sprites[direction]

    def get_current_sprite(self):
        return self.current_sprite

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
