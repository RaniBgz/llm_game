from model.entity import Entity

default_sprite = "./assets/default.png"

class Dialogue:
    def __init__(self, text, next_dialogue=None):
        self.text = text
        self.next_dialogue = next_dialogue

    def get_next_dialogue(self):
        return self.next_dialogue

class NPC(Entity):
    def __init__(self, name, hp, sprite=default_sprite, global_position=(0, 0), local_position=(0, 0), hostile=False):
        super().__init__()
        self.name = name
        self.hp = hp
        self.sprite = sprite
        self.global_position = global_position
        self.local_position = local_position
        self.hostile = hostile
        self.dead = False
        self.quests = []
        self.dialogue = []


    def get_id(self):
        return self.id

    def set_location(self, map, x, y):
        self.current_map = map
        self.x = x
        self.y = y

    def set_sprite(self, sprite):
        self.sprite = sprite

    def respawn(self):
        self.dead = False
