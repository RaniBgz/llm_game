from model.entity import Entity
from model.dialogue.dialogue import Dialogue
from model.dialogue.dialogue import QuestDialogue
# from model.subject.npc_subject import NPCSubject
from model.subject.subject import Subject

default_sprite = "./assets/default.png"


class NPC(Entity, Subject):
    def __init__(self,
                 name,
                 hp,
                 robot=False,
                 sprite=default_sprite,
                 global_position=(0, 0),
                 local_position=(0, 0),
                 hostile=False,
                 embedding=None):
        Entity.__init__(self)
        Subject.__init__(self)
        self.name = name
        self.hp = hp
        self.sprite = sprite
        self.robot = robot
        self.global_position = global_position
        self.local_position = local_position
        self.hostile = hostile
        self.dead = False
        self.embedding = embedding
        self.quests = []
        self.dialogue = []
        self.quests_dialogue = {}

    def notify(self, *args, **kwargs):
        for observer in self._observers:
            observer.update(self, *args, **kwargs)

    def get_id(self):
        return self.id

    def add_dialogue(self, dialogue):
        self.dialogue.append(dialogue)

    def get_quest_dialogue(self, quest_id):
        return self.quests_dialogue[quest_id]

    def set_location(self, map, x, y):
        self.current_map = map
        self.x = x
        self.y = y

    def set_sprite(self, sprite):
        self.sprite = sprite

    def kill(self):
        self.dead = True
        self.notify(self, "npc_dead")

    def respawn(self):
        self.dead = False
        self.notify(self, "npc_respawned")


    def add_quest_with_dialogue(self, quest, dialogue):
        self.quests.append(quest)
        quest_id = quest.get_id()
        self.quests_dialogue[quest_id] = dialogue
        print(f"Quest dialogue: {self.quests_dialogue}")

