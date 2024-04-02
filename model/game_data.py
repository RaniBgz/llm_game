from model.map.map import Map
from model.quest.quest_builder import QuestBuilder
from model.map.world_map import WorldMap

#TODO: Should the game data take as input a map? (map dimensions for now)
class GameData:
    def __init__(self):
        print("GameData initialized")
        self.character = None
        self.world_map = WorldMap.get_instance()
        self.initialize_world()
        self.npcs = []
        self.items = []

    def initialize_world(self):
        self.world_map.build_map(20, 20)

    def add_npc(self, npc):
        self.npcs.append(npc)
        self.world_map.add_entity(npc, npc.global_position)

    def add_item(self, item):
        self.items.append(item)
        self.world_map.add_entity(item, item.global_position)

    def set_character(self, character):
        self.character = character
        self.world_map.add_entity(character, character.global_position)

    def find_npc_by_id(self, id):
        for npc in self.npcs:
            if npc.id == id:
                return npc
        return None

    def find_npc_by_name(self, name):
        for npc in self.npcs:
            if npc.name == name:
                return npc
        return None

    def find_item_by_id(self, id):
        for item in self.items:
            if item.id == id:
                return item
        return None

    def find_item_by_name(self, name):
        for item in self.items:
            if item.name == name:
                return item
        return None
