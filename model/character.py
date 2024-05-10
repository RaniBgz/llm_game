""" Defines the character class that is used to define """
from model.entity import Entity
import pygame
import view.view_constants as view_cst
import json
from model.quest.quest import Quest
from model.item import Item
from model.subject.subject import Subject


class Character(Entity, Subject):
    def __init__(self, name,
                 hp,
                 global_position=(0, 0),
                 local_position=(0, 0),
                 sprite="./assets/sprites/character/character_idle_up.png",
                 embedding=None):
        Entity.__init__(self)
        Subject.__init__(self)
        self.name = name
        self.hp = hp
        self.sprite = sprite
        self.directions = ["up", "down", "left", "right"]
        self.sates = ["idle", "walking"]
        self.direction = "down"
        self.state = "idle"
        self.frame_index = 1
        self.idle_sprites = {}
        self.initialize_idle_sprites()
        self.walking_sprites = {}
        self.initialize_walking_sprites()
        # self.walking_sprites = {
        #     "down": [f"./assets/sprites/character/character_walk_down_{i}.png" for i in range(1, 6)],
        #     "up": [f"./assets/sprites/character/character_walk_up_{i}.png" for i in range(1, 6)],
        #     "left": [f"./assets/sprites/character/character_walk_left_{i}.png" for i in range(1, 6)],
        #     "right": [f"./assets/sprites/character/character_walk_right_{i}.png" for i in range(1, 6)]
        # }
        self.current_sprite = self.idle_sprites["down"]
        self.inventory = []
        self.quests = []
        self.global_position = global_position
        self.local_position = local_position
        self.embedding = embedding

    def notify(self, *args, **kwargs):
        for observer in self._observers:
            observer.update(self, *args, **kwargs)

    def initialize_idle_sprites(self):
        for direction in self.directions:
            sprite_path = f"./assets/sprites/character/character_idle_{direction}.png"
            self.idle_sprites[direction] = pygame.image.load(sprite_path).convert_alpha()
            self.idle_sprites[direction] = pygame.transform.scale(self.idle_sprites[direction], (view_cst.TILE_WIDTH, view_cst.TILE_HEIGHT))
            # self.current_direction = direction

    def initialize_walking_sprites(self):
        for direction in self.directions:
            self.walking_sprites[direction] = {}
            for i in range(1, 7):
                sprite_path = f"./assets/sprites/character/character_walk_{direction}_{i}.png"
                self.walking_sprites[direction][i] = pygame.image.load(sprite_path).convert_alpha()
                self.walking_sprites[direction][i] = pygame.transform.scale(self.walking_sprites[direction][i], (view_cst.TILE_WIDTH, view_cst.TILE_HEIGHT))

    def update_animation(self):
        if self.state == "idle":
            self.current_sprite = self.idle_sprites[self.direction]
        elif self.state == "walking":
            sprites = self.walking_sprites[self.direction]
            self.current_sprite = sprites[self.frame_index]
            self.frame_index = self.frame_index + 1
            if self.frame_index > len(sprites):
                self.frame_index = 1
        self.notify(self, "character_sprite_change", self.current_sprite, self.state, self.direction)

    def update_state(self, state):
        if state in self.sates:
            self.state = state
            # self.notify(self, "character_state_change", state)

    def update_direction(self, direction):
        if direction in self.directions:
            self.direction = direction
            self.frame_index = 1
            # self.current_sprite = self.idle_sprites[direction]
            # self.notify(self, "character_direction_change", self.current_sprite, direction)

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
