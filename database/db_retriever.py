from database.db_builder import Character, NPC, Item, Quest, Objective, KillObjective, LocationObjective, RetrievalObjective
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from model.character import Character
from model.npc import NPC
from model.item import Item
from model.quests.quest import Quest
from model.quests.objective import Objective, KillObjective, LocationObjective, RetrievalObjective

engine = create_engine('postgresql+psycopg2://rani:ranidb@localhost/llmgame')
Base = declarative_base()

def initialize_session():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def retrieve_characters(session):
    characters = session.query(Character).all()
    for character in characters:
        print(f"Character: {character.name}, HP: {character.hp}, Global: {character.global_position}, Local: {character.local_position}")
        # Instantiate an object of the Character class for each record
        character_obj = Character(name=character.name, hp=character.hp, global_position=character.global_position, local_position=character.local_position)
        print(f"Object instantiated: {character_obj}\n")

def retrieve_npcs(session):
    npcs = session.query(NPC).all()
    for npc in npcs:
        print(f"NPC: {npc.name}, HP: {npc.hp}, Hostile: {npc.hostile}, Global: {npc.global_position}, Local: {npc.local_position}")
        # Instantiate an object of the NPC class for each record
        npc_obj = NPC(name=npc.name, hp=npc.hp, hostile=npc.hostile, global_position=npc.global_position, local_position=npc.local_position)
        print(f"Object instantiated: {npc_obj}\n")

def retrieve_items(session):
    items = session.query(Item).all()
    for item in items:
        print(f"Item ID: {item.id}, Character ID: {item.character_id}")
        # Instantiate an object of the Item class for each record
        item_obj = Item(id=item.id, character_id=item.character_id)
        print(f"Object instantiated: {item_obj}\n")

def retrieve_quests(session):
    quests = session.query(Quest).all()
    for quest in quests:
        print(f"Quest: {quest.name}, Active: {quest.active}, Description: {quest.description}")
        # Instantiate an object of the Quest class for each record
        quest_obj = Quest(name=quest.name, description=quest.description, active=quest.active)
        print(f"Object instantiated: {quest_obj}\n")

def retrieve_objectives(session):
    objectives = session.query(Objective).all()
    for objective in objectives:
        print(f"Objective ID: {objective.id}, Quest ID: {objective.quest_id}, Type: {objective.type}")
        # Note: Instantiating the right subclass based on the type
        if objective.type == 'kill':
            objective_obj = KillObjective(target_id=objective.target_id)
        elif objective.type == 'location':
            objective_obj = LocationObjective(target_location=objective.target_location)
        elif objective.type == 'retrieval':
            objective_obj = RetrievalObjective(target_item_id=objective.target_item_id)
        else:
            objective_obj = Objective()
        print(f"Object instantiated: {objective_obj}\n")

if __name__ == '__main__':
    session = initialize_session()
    retrieve_characters(session)
    retrieve_npcs(session)
    retrieve_items(session)
    retrieve_quests(session)
    retrieve_objectives(session)
