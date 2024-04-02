from database.db_builder import (Character as DBCharacter, NPC as DBNPC, Item as DBItem)
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from model.character import Character
from model.npc import NPC
from model.item import Item

engine = create_engine('postgresql+psycopg2://rani:ranidb@localhost/llmgame')
Base = declarative_base()

def initialize_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def retrieve_characters():
    session = initialize_session()
    characters = session.query(DBCharacter).all()
    characters_list = []
    for character in characters:
        game_character = convert_sqlalchemy_character_to_game_character(character)
        characters_list.append(game_character)
        print(f"Character: {game_character.name}, HP: {game_character.hp}, Global: {game_character.global_position}, Local: {game_character.local_position}",
              f"Sprite: {game_character.sprite}")
        print(f"Object instantiated: {game_character}\n")
    return characters_list

def retrieve_items():
    session = initialize_session()
    items = session.query(DBItem).all()
    items_list = []
    for item in items:
        game_item = convert_sqlalchemy_item_to_game_item(item)
        items_list.append(game_item)
        print(f"Item ID: {game_item.id}, Name: {game_item.name}, Description: {game_item.description}, sprite: {game_item.sprite},")
        print(f"Object instantiated: {game_item}\n")
    return items_list

def retrieve_npcs():
    session = initialize_session()
    npcs = session.query(DBNPC).all()
    npcs_list = []
    for npc in npcs:
        game_npc = convert_sqlalchemy_npc_to_game_npc(npc)
        npcs_list.append(game_npc)
        print(f"NPC: {game_npc.name}, HP: {game_npc.hp}, Hostile: {game_npc.hostile},"
              f"Global: {game_npc.global_position}, Local: {game_npc.local_position}")
        print(f"Object instantiated: {game_npc}\n")
    return npcs_list

def convert_sqlalchemy_character_to_game_character(sqlalchemy_character):
    """Converts a SQLAlchemy Character instance to a game model Character instance."""
    return Character(
        name=sqlalchemy_character.name,
        hp=sqlalchemy_character.hp,
        global_position=tuple(map(int, sqlalchemy_character.global_position.split(','))),
        local_position=tuple(map(int, sqlalchemy_character.local_position.split(','))),
        sprite=sqlalchemy_character.sprite,
    )

def convert_sqlalchemy_npc_to_game_npc(sqlalchemy_npc):
    """Converts a SQLAlchemy NPC instance to a game model NPC instance."""
    return NPC(
        name=sqlalchemy_npc.name,
        hp=sqlalchemy_npc.hp,
        sprite=sqlalchemy_npc.sprite,
        global_position=tuple(map(int, sqlalchemy_npc.global_position.split(','))),
        local_position=tuple(map(int, sqlalchemy_npc.local_position.split(','))),
        hostile=sqlalchemy_npc.hostile,
    )

def convert_sqlalchemy_item_to_game_item(sqlalchemy_item):
    """Converts a SQLAlchemy Item instance to a game model Item instance."""
    # Assuming the game model Item constructor takes an id and character_id
    return Item(name=sqlalchemy_item.name,
                description=sqlalchemy_item.description,
                global_position=tuple(map(int, sqlalchemy_item.global_position.split(','))),
                local_position=tuple(map(int, sqlalchemy_item.local_position.split(','))),
                sprite=sqlalchemy_item.sprite)


if __name__ == '__main__':
    session = initialize_session()
    retrieve_characters(session)
    retrieve_npcs(session)
    retrieve_items(session)

