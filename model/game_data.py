from model.map.map import Map
from model.quest.quest_builder import QuestBuilder
from model.map.world_map import WorldMap
from ai.old_llm.llm_model import LLMModel
import database.utils as utils
from sentence_transformers import SentenceTransformer, util

#TODO: Should the game data take as input a map? (map dimensions for now)
class GameData:
    def __init__(self):
        print("GameData initialized")
        self.character = None
        self.world_map = WorldMap.get_instance()
        self.initialize_world()
        self.llm_model = LLMModel("gpt-3.5-turbo-1106")
        self.embedding_model = SentenceTransformer('all-miniLM-L6-v2')
        self.npcs = []
        self.items = []
        self.quests = []
        self.game_context = ''

    def initialize_world(self):
        self.world_map.build_map(20, 20)

    def embed_text(self, text):
        return self.embedding_model.encode(text, convert_to_numpy=True)

    #TODO: this may change a lot in the future
    def get_llm_model(self):
        return self.llm_model

    def set_llm_model(self, model):
        self.llm_model = model

    def set_character(self, character):
        self.character = character
        self.world_map.add_entity(character, character.global_position)

    def set_game_context(self, context):
        self.game_context = context

    def get_game_context(self):
        return self.game_context

    def add_npc(self, npc):
        self.npcs.append(npc)
        self.world_map.add_entity(npc, npc.global_position)

    def add_item(self, item):
        self.items.append(item)
        self.world_map.add_entity(item, item.global_position)

    def add_quest(self, quest):
        self.quests.append(quest)

    def find_most_similar_npc(self, name):
        name_vector = self.embed_text(name)
        max_similarity = -1
        most_similar_npc = None
        for npc in self.npcs:
            cosine_similarity = util.cos_sim(name_vector, npc.embedding)
            if cosine_similarity > max_similarity:
                max_similarity = cosine_similarity
                most_similar_npc = npc
        return most_similar_npc

    def find_most_similar_friendly_npc(self, name):
        name_vector = self.embed_text(name)
        max_similarity = -1
        most_similar_npc = None
        for npc in self.npcs:
            if npc.hostile:
                continue
            else:
                cosine_similarity = util.cos_sim(name_vector, npc.embedding)
                if cosine_similarity > max_similarity:
                    max_similarity = cosine_similarity
                    most_similar_npc = npc
        return most_similar_npc

    def find_most_similar_hostile_npc(self, name):
        name_vector = self.embed_text(name)
        max_similarity = -1
        most_similar_npc = None
        for npc in self.npcs:
            if not npc.hostile:
                continue
            else:
                cosine_similarity = util.cos_sim(name_vector, npc.embedding)
                if cosine_similarity > max_similarity:
                    max_similarity = cosine_similarity
                    most_similar_npc = npc
        return most_similar_npc


    def find_most_similar_item(self, name):
        name_vector = self.embed_text(name)
        max_similarity = -1
        most_similar_item = None
        for item in self.items:
            if self.character.has_item(item):
                continue
            else:
                cosine_similarity = util.cos_sim(name_vector, item.embedding)
                if cosine_similarity > max_similarity:
                    max_similarity = cosine_similarity
                    most_similar_item = item
        return most_similar_item

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
            quest.set_not_ended()
            # quest.set_active()

    def reset_items(self):
        for item in self.items:
            item.reset_item()
            if item.in_world:
                self.character.remove_item_from_inventory(item)
                self.world_map.add_entity(item, item.global_position)