from model.map.map import Map

# Model (This would eventually hold game data and logic)


class GameData:  # Placeholder for now
    def __init__(self):
        self.character = None
        self.quest_builder = None

    def find_npc_by_id(self, id):
        for npc in self.npc_list:
            if npc.id == id:
                return npc
        return None


