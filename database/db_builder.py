import psycopg2
from sqlalchemy import create_engine
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declared_attr
from sqlalchemy.sql.schema import Table

engine = create_engine('postgresql+psycopg2://rani:ranidb@localhost/llmgame')
Base = declarative_base()

class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hp = Column(Integer)
    global_position = Column(String)  # Stored as "x,y"
    local_position = Column(String)  # Stored as "x,y"
    sprite = Column(String, default="./assets/sprites/character.png")
    # Relationships
    inventory = relationship("Item", backref="character")
    quests = relationship("Quest", backref="character")

class NPC(Base):
    __tablename__ = 'npcs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hp = Column(Integer)
    global_position = Column(String)  # Stored as "x,y"
    local_position = Column(String)  # Stored as "x,y"
    sprite = Column(String, default="./assets/default.png")
    hostile = Column(Boolean, default=False)  # Add this line

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'))

class Quest(Base):
    __tablename__ = 'quests'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'))
    name = Column(String)
    description = Column(String)
    active = Column(Boolean)
    # Relationship with objectives
    objectives = relationship("Objective", backref="quest")


class Objective(Base):
    __tablename__ = 'objectives'
    id = Column(Integer, primary_key=True)
    quest_id = Column(Integer, ForeignKey('quests.id'))  # Foreign key to Quest
    type = Column(String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'objective',
        'polymorphic_on': type,
    }

    def check_completion(self, player):
        raise NotImplementedError("Subclasses must implement check_completion method.")

class KillObjective(Objective):
    __mapper_args__ = {
        'polymorphic_identity': 'kill'
    }
    target_id = Column(Integer)  # Assuming target ID is an integer

    def check_completion(self, player):
        # Implementation specific to KillObjective
        pass

class LocationObjective(Objective):
    __mapper_args__ = {
        'polymorphic_identity': 'location'
    }
    target_location = Column(String)  # Storing location as a string, but could be more complex

    def check_completion(self, player):
        # Implementation specific to LocationObjective
        pass

class RetrievalObjective(Objective):
    __mapper_args__ = {
        'polymorphic_identity': 'retrieval'
    }
    target_item_id = Column(Integer)  # Assuming item ID is an integer

    def check_completion(self, player):
        # Implementation specific to RetrievalObjective
        pass

def load_database():
    print(f"Adding instances to the database")
    # First, create the database schema
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    character = Character(name='Hero', hp=100, global_position="1,1", local_position="2,2",
                          sprite="./assets/sprites/character.png")
    session.add(character)

    # Add 5 NPCs (2 friendly, 3 hostile)
    npcs = [
        NPC(name='Friendly NPC 1', hp=50, global_position="3,3", local_position="4,4", sprite="./assets/default.png",
            hostile=False),
        NPC(name='Friendly NPC 2', hp=50, global_position="5,5", local_position="6,6", sprite="./assets/default.png",
            hostile=False),
        NPC(name='Hostile NPC 1', hp=70, global_position="7,7", local_position="8,8", sprite="./assets/default.png",
            hostile=True),
        NPC(name='Hostile NPC 2', hp=70, global_position="9,9", local_position="10,10", sprite="./assets/default.png",
            hostile=True),
        NPC(name='Hostile NPC 3', hp=70, global_position="11,11", local_position="12,12", sprite="./assets/default.png",
            hostile=True),
    ]
    session.add_all(npcs)

    # Add 5 Items
    items = [
        Item(character_id=character.id),
        # Assuming Item has a character_id but not linked directly to character's inventory
        Item(character_id=character.id),
        Item(character_id=character.id),
        Item(character_id=character.id),
        Item(character_id=character.id),
    ]
    session.add_all(items)

    # Add 3 Quests with different Objectives
    quest1 = Quest(name="Quest 1", description="Kill Objective", active=True)
    quest1.objectives.append(KillObjective(target_id=1))

    quest2 = Quest(name="Quest 2", description="Location Objective", active=True)
    quest2.objectives.append(LocationObjective(target_location="13,13"))

    quest3 = Quest(name="Quest 3", description="Retrieval Objective", active=True)
    quest3.objectives.append(RetrievalObjective(target_item_id=1))

    session.add_all([quest1, quest2, quest3])

    # Commit everything to the database
    session.commit()

    # Close the session
    session.close()

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="llmgame",
            user="rani",  # replace with your PostgreSQL username
            password="ranidb",  # replace with your password
            host="localhost"
        )
    except psycopg2.Error as e:
        print("Unable to connect to the database")
        print(e)
    else:
        print("Connected to the database")
        return conn
def create_table(conn):
    cursor = conn.cursor()
    sql_create_table = """
    CREATE TABLE IF NOT EXISTS new_table (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """
    try:
        cursor.execute(sql_create_table)
    except psycopg2.Error as e:
        print("Error creating table")
        print(e)
    else:
        print("Table created successfully")
        conn.commit()

if __name__ == "__main__":
    load_database()
    # # Querying characters
    # hero = session.query(Character).filter_by(name="Hero").first()
    # print(hero.name)


    # conn = connect_to_db()
    # create_table(conn)
    # conn.close()