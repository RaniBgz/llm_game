import psycopg2
from model.character import Character
from model.npc import NPC
from model.item import Item
from sentence_transformers import SentenceTransformer
import numpy as np


class DBRetriever:
    def __init__(self):
        self.conn = self.connect_to_db()
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
            return conn


    def retrieve_character_by_name(self, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, hp, global_position, local_position, sprite FROM characters WHERE name = %s", (name,))
        character_data = cursor.fetchone()

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

    def retrieve_vectors_by_npc_name(self, npc_name):
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT id, name, embedding FROM npcs WHERE name = %s;", (npc_name,))
            rows = cursor.fetchall()
            if rows:
                vectors = [(row[0], np.array(row[2])) for row in rows if row[2] is not None]
                return vectors
            else:
                print("No NPCs found with this name")
                return None
        except psycopg2.Error as e:
            print("Error retrieving vectors from npcs:", e)
        finally:
            cursor.close()

    def retrieve_characters(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, hp, global_position, local_position, sprite FROM characters")
        characters = cursor.fetchall()
        characters_list = []
        for character in characters:
            name, hp, global_position, local_position, sprite = character
            global_position = tuple(map(int, global_position.split(',')))
            local_position = tuple(map(int, local_position.split(',')))
            game_character = Character(name, hp, global_position, local_position, sprite)
            characters_list.append(game_character)
            print(f"Character: {game_character.name}, HP: {game_character.hp}, Global: {game_character.global_position}, Local: {game_character.local_position}",
                  f"Sprite: {game_character.sprite}")
            print(f"Object instantiated: {game_character}\n")
        return characters_list

    def retrieve_items(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, description, global_position, local_position, sprite, in_world FROM items")
        items = cursor.fetchall()
        items_list = []
        for item in items:
            id, name, description, global_position, local_position, sprite, in_world = item
            global_position = tuple(map(int, global_position.split(',')))
            local_position = tuple(map(int, local_position.split(',')))
            game_item = Item(name, description, global_position=global_position, local_position=local_position, sprite=sprite, in_world=in_world)
            items_list.append(game_item)
            print(f"Item ID: {game_item.id}, Name: {game_item.name}, Description: {game_item.description},  sprite: {game_item.sprite}. In world: {game_item.in_world}")
            print(f"Object instantiated: {game_item}\n")
        return items_list

    def retrieve_npcs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, hp, robot, global_position, local_position, sprite, hostile FROM npcs")
        npcs = cursor.fetchall()
        npcs_list = []
        for npc in npcs:
            name, hp, robot, global_position, local_position, sprite, hostile = npc
            global_position = tuple(map(int, global_position.split(',')))
            local_position = tuple(map(int, local_position.split(',')))
            game_npc = NPC(name, hp, robot, sprite, global_position, local_position, hostile)
            npcs_list.append(game_npc)
            print(f"NPC: {game_npc.name}, HP: {game_npc.hp}, Hostile: {game_npc.hostile},"
                  f"Global: {game_npc.global_position}, Local: {game_npc.local_position}")
            print(f"Object instantiated: {game_npc}\n")
        return npcs_list


    def close_connection(self):
        self.conn.close()

if __name__ == '__main__':
    db_retriever = DBRetriever()
    db_retriever.retrieve_npc_by_name("Elder")
    db_retriever.retrieve_character_by_name("Gary")
    db_retriever.retrieve_item_by_name("Health Potion")
    # retrieve_characters()
    # retrieve_npcs()
    # retrieve_items()
    db_retriever.close_connection()


