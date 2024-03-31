from model.map.map import Map
from model.quest.quest_builder import QuestBuilder
from model.map.world_map import WorldMap

# Model (This would eventually hold game data and logic)


class GameData:  # Placeholder for now
    def __init__(self):
        self.character = None
        self.world_map = WorldMap.get_instance()
        self.quest_builder = QuestBuilder()
        self.npcs = []

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

    def check_npc_dead(self, id):
        npc = self.find_npc_by_id(id)
        if npc.dead:
            return True
        return False


