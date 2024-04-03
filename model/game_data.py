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
        self.quests = []

    def initialize_world(self):
        self.world_map.build_map(20, 20)

    def add_npc(self, npc):
        self.npcs.append(npc)
        self.world_map.add_entity(npc, npc.global_position)

    def add_item(self, item):
        self.items.append(item)
        self.world_map.add_entity(item, item.global_position)

    def add_quest(self, quest):
        self.quests.append(quest)

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

    def find_quest_by_id(self, id):
        for quest in self.quests:
            if quest.id == id:
                return quest
        return None

    def find_quest_by_name(self, name):
        for quest in self.quests:
            if quest.name == name:
                return quest
        return None

    def respawn_mobs(self):
        for npc in self.npcs:
            if npc.hostile:
                if npc.dead:
                    npc.respawn()
    def respawn_npcs(self):
        #To be implemented, for now, friendly npcs can't be killed
        pass

    def reset_quests(self):
        print(f"Len quests: {len(self.quests)}")
        for quest in self.quests:
            for objective in quest.objectives:
                objective.set_not_completed()
            quest.set_not_completed()

    def reset_items(self):
        for item in self.items:
            item.reset_item()
            if item.in_world:
                self.character.remove_item_from_inventory(item)
                self.world_map.add_entity(item, item.global_position)