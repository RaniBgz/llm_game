import psycopg2
from model.character import Character
from model.npc import NPC
from model.item import Item
from sentence_transformers import SentenceTransformer, util
import database.utils as utils
import numpy as np


class DBRetriever:
    def __init__(self):
        self.conn = None
        # self.conn = self.connect_to_db()
        self.embedding_model = SentenceTransformer('all-miniLM-L6-v2')

    def connect_to_db(self):
        try:
            conn = psycopg2.connect(
                dbname="llmgame",
                user="rani",
                password="ranidb",
                host="localhost"
            )
        except psycopg2.Error as e:
            print("Unable to connect to the database")
            print(e)
        else:
            print("Connected to the database")
            self.conn = conn
            return conn

    def embed_text(self, text):
        return self.embedding_model.encode(text, convert_to_numpy=True)

    def ensure_connection(self):
        try:
            # psycopg2 exposes the closed attribute which is False if the connection is open
            if self.conn.closed:
                print("Reconnecting to the database...")
                self.conn = self.connect_to_db()
        except psycopg2.Error as e:
            print("Error checking database connection:", e)

    '''Retrieve by name functions for characters, NPCs and items.
    Need to add embedding'''
    def retrieve_character_by_name(self, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, hp, global_position, local_position, sprite FROM characters WHERE name = %s", (name,))
        character_data = cursor.fetchone()
        cursor.close()

        if character_data:
            name, hp, global_position, local_position, sprite = character_data
            global_position = tuple(map(int, global_position.split(',')))
            local_position = tuple(map(int, local_position.split(',')))
            game_character = Character(name, hp, global_position, local_position, sprite)
            print(f"Retrieved Character: {game_character.name} with HP: {game_character.hp}")
            return game_character
        else:
            print("Character not found")
            return None

    def retrieve_npc_by_name(self, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, hp, robot, global_position, local_position, sprite, hostile FROM npcs WHERE name = %s", (name,))
        npc_data = cursor.fetchone()
        cursor.close()

        if npc_data:
            name, hp, robot, global_position, local_position, sprite, hostile = npc_data
            global_position = tuple(map(int, global_position.split(',')))
            local_position = tuple(map(int, local_position.split(',')))
            game_npc = NPC(name, hp, robot, sprite, global_position, local_position, hostile)
            print(f"Retrieved NPC: {game_npc.name} with HP: {game_npc.hp} and Hostility: {game_npc.hostile}")
            return game_npc
        else:
            print("NPC not found")
            return None

    def retrieve_item_by_name(self, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, description, global_position, local_position, sprite, in_world FROM items WHERE name = %s", (name,))
        item_data = cursor.fetchone()
        cursor.close()

        if item_data:
            id, name, description, global_position, local_position, sprite, in_world = item_data
            global_position = tuple(map(int, global_position.split(',')))
            local_position = tuple(map(int, local_position.split(',')))
            game_item = Item(name, description, global_position=global_position, local_position=local_position, sprite=sprite, in_world=in_world)
            print(f"Retrieved Item: {game_item.name} with Description: {game_item.description}")
            return game_item
        else:
            print("Item not found")
            return None

    '''Retrieve vectors by name functions for characters, NPCs and items.
    Need to add embedding'''
    def retrieve_vectors_by_character_name(self, character_name):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT id, name, embedding FROM characters WHERE name = %s;", (character_name,))
            rows = cursor.fetchall()
            if rows:
                # vectors = [(row[0], np.array(row[2])) for row in rows if row[2] is not None]
                vectors = [(row[0], utils.string_to_np_array(row[2])) for row in rows if row[2] is not None]
                return vectors
            else:
                print("No characters found with this name")
                return None
        except psycopg2.Error as e:
            print("Error retrieving vectors from characters:", e)
        finally:
            cursor.close()

    def retrieve_vectors_by_npc_name(self, npc_name):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT id, name, embedding FROM npcs WHERE name = %s;", (npc_name,))
            rows = cursor.fetchall()
            if rows:
                # vectors = [(row[0], np.array(row[2])) for row in rows if row[2] is not None]
                vectors = [(row[0], utils.string_to_np_array(row[2])) for row in rows if row[2] is not None]
                return vectors
            else:
                print("No NPCs found with this name")
                return None
        except psycopg2.Error as e:
            print("Error retrieving vectors from npcs:", e)
        finally:
            cursor.close()

    def retrieve_vectors_by_item_name(self, item_name):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT id, name, embedding FROM items WHERE name = %s;", (item_name,))
            rows = cursor.fetchall()
            if rows:
                # vectors = [(row[0], np.array(row[2])) for row in rows if row[2] is not None]
                vectors = [(row[0], utils.string_to_np_array(row[2])) for row in rows if row[2] is not None]
                return vectors
            else:
                print("No items found with this name")
                return None
        except psycopg2.Error as e:
            print("Error retrieving vectors from items:", e)
        finally:
            cursor.close()

    def retrieve_characters(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, hp, global_position, local_position, sprite, embedding FROM characters")
        characters = cursor.fetchall()
        cursor.close()
        characters_list = []
        for character in characters:
            name, hp, global_position, local_position, sprite, embedding = character
            embedding = utils.string_to_np_array(embedding)
            global_position = tuple(map(int, global_position.split(',')))
            local_position = tuple(map(int, local_position.split(',')))
            game_character = Character(name,
                                       hp,
                                       global_position,
                                       local_position,
                                       sprite=sprite,
                                       embedding=embedding)
            characters_list.append(game_character)
            print(f"Character: {game_character.name}, HP: {game_character.hp}, Global: {game_character.global_position}, Local: {game_character.local_position}",
                  f"Sprite: {game_character.sprite}")
            print(f"Object instantiated: {game_character}\n")
        return characters_list

    def retrieve_items(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, description, global_position, local_position, sprite, in_world, embedding FROM items")
        items = cursor.fetchall()
        cursor.close()
        items_list = []
        for item in items:
            id, name, description, global_position, local_position, sprite, in_world, embedding = item
            embedding = utils.string_to_np_array(embedding)
            global_position = tuple(map(int, global_position.split(',')))
            local_position = tuple(map(int, local_position.split(',')))
            game_item = Item(name,
                             description,
                             global_position=global_position,
                             local_position=local_position,
                             sprite=sprite,
                             in_world=in_world,
                             embedding=embedding)
            items_list.append(game_item)
            print(f"Item ID: {game_item.id}, Name: {game_item.name}, Description: {game_item.description},  sprite: {game_item.sprite}. In world: {game_item.in_world}")
            print(f"Object instantiated: {game_item}\n")
        return items_list

    def retrieve_npcs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, hp, robot, global_position, local_position, sprite, hostile, embedding FROM npcs")
        npcs = cursor.fetchall()
        cursor.close()
        npcs_list = []
        for npc in npcs:
            name, hp, robot, global_position, local_position, sprite, hostile, embedding = npc
            embedding = utils.string_to_np_array(embedding)
            global_position = tuple(map(int, global_position.split(',')))
            local_position = tuple(map(int, local_position.split(',')))
            game_npc = NPC(name,
                           hp,
                           robot,
                           sprite=sprite,
                           global_position=global_position,
                           local_position=local_position,
                           hostile=hostile,
                           embedding=embedding)
            npcs_list.append(game_npc)
            print(f"NPC: {game_npc.name}, HP: {game_npc.hp}, Hostile: {game_npc.hostile},"
                  f"Global: {game_npc.global_position}, Local: {game_npc.local_position}")
            print(f"Object instantiated: {game_npc}\n")
        return npcs_list


    def close_connection(self):
        self.conn.close()

if __name__ == '__main__':
    db_retriever = DBRetriever()
    # db_retriever.retrieve_npc_by_name("Elder")
    # db_retriever.retrieve_character_by_name("Gary")
    # db_retriever.retrieve_item_by_name("Health Potion")
    npc_1 = db_retriever.retrieve_vectors_by_npc_name("Elder")
    npc_2 = db_retriever.retrieve_vectors_by_npc_name("Enchantress")
    npc_3 = db_retriever.retrieve_vectors_by_npc_name("Echo")
    npc_4 = db_retriever.retrieve_vectors_by_npc_name("Goblin")
    npc_5 = db_retriever.retrieve_vectors_by_npc_name("Skeleton")
    cosine_sim_1_2 = util.cos_sim(npc_1[0][1], npc_2[0][1])
    cosine_sim_1_3 = util.cos_sim(npc_1[0][1], npc_3[0][1])
    cosine_sim_1_4 = util.cos_sim(npc_1[0][1], npc_4[0][1])
    cosine_sim_1_5 = util.cos_sim(npc_1[0][1], npc_5[0][1])
    cosine_sim_2_3 = util.cos_sim(npc_2[0][1], npc_3[0][1])
    cosine_sim_2_4 = util.cos_sim(npc_2[0][1], npc_4[0][1])
    cosine_sim_2_5 = util.cos_sim(npc_2[0][1], npc_5[0][1])
    cosine_sim_3_4 = util.cos_sim(npc_3[0][1], npc_4[0][1])
    cosine_sim_3_5 = util.cos_sim(npc_3[0][1], npc_5[0][1])
    cosine_sim_4_5 = util.cos_sim(npc_4[0][1], npc_5[0][1])


    print(f"Cosine similarity Elder - Enchantress : {cosine_sim_1_2.item()}")
    print(f"Cosine similarity Elder - Echo : {cosine_sim_1_3.item()}")
    print(f"Cosine similarity Elder - Goblin : {cosine_sim_1_4.item()}")
    print(f"Cosine similarity Elder - Skeleton : {cosine_sim_1_5.item()}")
    print(f"Cosine similarity Enchantress - Echo : {cosine_sim_2_3.item()}")
    print(f"Cosine similarity Enchantress - Goblin : {cosine_sim_2_4.item()}")
    print(f"Cosine similarity Enchantress - Skeleton : {cosine_sim_2_5.item()}")
    print(f"Cosine similarity Echo - Goblin : {cosine_sim_3_4.item()}")
    print(f"Cosine similarity Echo - Skeleton : {cosine_sim_3_5.item()}")
    print(f"Cosine similarity Goblin - Skeleton : {cosine_sim_4_5.item()}")

    # retrieve_characters()
    # retrieve_npcs()
    # retrieve_items()
    db_retriever.close_connection()


    # def retrieve_most_similar_npc(self, npc_name):
    #     cursor = self.conn.cursor()
    #     try:
    #         cursor.execute("SELECT id, name, embedding FROM npcs;")
    #         cursor.execute("SELECT name, hp, robot, global_position, local_position, sprite, hostile, embedding FROM npcs")
    #         rows = cursor.fetchall()
    #         if rows:
    #             most_similar_npc_name = ""
    #             max_similarity = -1
    #             npc_name_vector = self.embed_text(npc_name)
    #             vectors = [(row[0], utils.string_to_np_array(row[2])) for row in rows if row[2] is not None]
    #             #TODO: fix from here
    #             #If there are several NPCs with the same name, we need to compare the embeddings for each one
    #             for vector in vectors:
    #                 np_vector = vector[2]
    #                 cosine_similarity = util.cos_sim(npc_name_vector, np_vector)
    #                 if cosine_similarity > max_similarity:
    #                     max_similarity = cosine_similarity
    #                     most_similar_npc_name = str(vector[1])
    #         else:
    #             print("No NPCs found")
    #             return None
    #     except psycopg2.Error as e:
    #         print("Error retrieving vectors from npcs:", e)
    #     finally:
    #         cursor.close()
    #         #Build NPC object from most_similar_npc_name
