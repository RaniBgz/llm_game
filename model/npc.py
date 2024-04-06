from model.entity import Entity
from model.dialogue import Dialogue
from model.dialogue import QuestDialogue

default_sprite = "./assets/default.png"


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
        self.quests_dialogue = {}

    def get_id(self):
        return self.id

    def add_dialogue(self, dialogue):
        self.dialogue.append(dialogue)

    def set_location(self, map, x, y):
        self.current_map = map
        self.x = x
        self.y = y

    def set_sprite(self, sprite):
        self.sprite = sprite

    def respawn(self):
        self.dead = False

    def add_quest_with_dialogue(self, quest, dialogue):
        self.quests.append(quest)
        quest_id = quest.get_id()
        self.quests_dialogue[quest_id] = dialogue
        print(f"Quest dialogue: {self.quests_dialogue}")

