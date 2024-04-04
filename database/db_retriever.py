import psycopg2
from model.character import Character
from model.npc import NPC
from model.item import Item



def connect_to_db():
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

def retrieve_characters():
    conn = connect_to_db()
    cursor = conn.cursor()
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

def retrieve_items():
    conn = connect_to_db()
    cursor = conn.cursor()
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

def retrieve_npcs():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, hp, global_position, local_position, sprite, hostile FROM npcs")
    npcs = cursor.fetchall()
    npcs_list = []
    for npc in npcs:
        name, hp, global_position, local_position, sprite, hostile = npc
        global_position = tuple(map(int, global_position.split(',')))
        local_position = tuple(map(int, local_position.split(',')))
        game_npc = NPC(name, hp, sprite, global_position, local_position, hostile)
        npcs_list.append(game_npc)
        print(f"NPC: {game_npc.name}, HP: {game_npc.hp}, Hostile: {game_npc.hostile},"
              f"Global: {game_npc.global_position}, Local: {game_npc.local_position}")
        print(f"Object instantiated: {game_npc}\n")
    return npcs_list

if __name__ == '__main__':
    conn = connect_to_db()
    retrieve_characters()
    retrieve_npcs()
    retrieve_items()
    conn.close()

