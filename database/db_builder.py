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
    type = Column(String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'objective',
        'polymorphic_on': type
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
    pass
    # Base.metadata.create_all(engine)
    # Session = sessionmaker(bind=engine)
    # session = Session()
    #
    # # Inserting a new character
    # new_character = Character(name="Hero", hp=100)
    # session.add(new_character)
    # session.commit()
    #
    # # Querying characters
    # hero = session.query(Character).filter_by(name="Hero").first()
    # print(hero.name)


    # conn = connect_to_db()
    # create_table(conn)
    # conn.close()