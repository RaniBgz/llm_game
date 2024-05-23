from model.entity import Entity
from model.dialogue.dialogue import Dialogue
from model.dialogue.dialogue import QuestDialogue
# from model.subject.npc_subject import NPCSubject
from model.subject.subject import Subject
import networkx as nx

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
        self.friendship_graph = nx.Graph()
        self.family_graph = nx.DiGraph()

    def add_friendship(self, other_npc):
        self.friendship_graph.add_edge(self.name, other_npc.name, relationship="friend")

    def add_family_tie(self, other_npc, relationship_type):
        self.family_graph.add_edge(self.name, other_npc.name, relationship=relationship_type)
        # Adding the inverse relationship if necessary
        inverse_relationship = {
            "grandfather": "granddaughter",
            "grandmother": "grandson",  # and vice versa
            "father": "son",
            "mother": "daughter",  # add more as needed
            # You can extend this dictionary with more relationships
        }.get(relationship_type, None)

        if inverse_relationship:
            self.family_graph.add_edge(other_npc.name, self.name, relationship=inverse_relationship)

    def get_friendships(self):
        return self.friendship_graph.edges(data=True)

    def get_family_ties(self):
        return self.family_graph.edges(data=True)

    def get_related_friends(self, level=1):
        return list(nx.single_source_shortest_path_length(self.friendship_graph, self.name, cutoff=level).keys())

    def get_related_family(self, level=1):
        return list(nx.single_source_shortest_path_length(self.family_graph, self.name, cutoff=level).keys())

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
        # print(f"Quest dialogue: {self.quests_dialogue}")


if __name__ == "__main__":
    npc1 = NPC(name="Elder", hp=100)
    npc2 = NPC(name="Enchantress", hp=100)

    # Add family relationship
    npc1.add_family_tie(npc2, "grandfather")

    # Get family relationships
    print(npc1.get_family_ties())
    # Outputs: [('Elder', 'Enchantress', {'relationship': 'grandfather'}), ('Enchantress', 'Elder', {'relationship': 'granddaughter'})]

    # Search related family within 1 level deep
    print(npc1.get_related_family(level=1))  # Outputs: ['Elder', 'Enchantress']