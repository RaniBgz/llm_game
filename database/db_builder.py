import psycopg2
from sqlalchemy import update
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy.orm import declared_attr
# from sqlalchemy.sql.schema import Table
import view.view_constants as view_cst

engine = create_engine('postgresql+psycopg2://rani:ranidb@localhost/llmgame')
Base = declarative_base()

#TODO: will need methods to update some attributes of an object
#TODO: How to handle quests and objective. May not need to store objectives since th

class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hp = Column(Integer)
    global_position = Column(String)  #"x,y"
    local_position = Column(String)  #"x,y"
    sprite = Column(String, default="./assets/sprites/character.png")

class NPC(Base):
    __tablename__ = 'npcs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hp = Column(Integer)
    global_position = Column(String)  #"x,y"
    local_position = Column(String)  #"x,y
    sprite = Column(String, default="./assets/default.png")
    hostile = Column(Boolean, default=False)

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    global_position = Column(String)  #"x,y"
    local_position = Column(String)  #"x,y"
    sprite = Column(String, default="./assets/default.png")

def load_database():
    print(f"Adding instances to the database")
    # First, create the database schema
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    character = Character(name='Gary', hp=16, global_position="0,0", local_position=f"{view_cst.H_TILES//2},{view_cst.V_TILES-1}",
                          sprite="./assets/sprites/character/character.png")
    session.add(character)

    # Add 5 NPCs (2 friendly, 3 hostile)
    npcs = [
        NPC(name='Elder', hp=1000, global_position="0,0", local_position=f"{view_cst.H_TILES//3},1", sprite="./assets/sprites/npcs/elder.png",
            hostile=False),
        NPC(name='Robot', hp=10000, global_position="0,0", local_position=f"{2*view_cst.H_TILES//3},1", sprite="./assets/sprites/npcs/robot.png",
            hostile=False),
        NPC(name='Plant', hp=8, global_position="0,1", local_position=f"{view_cst.H_TILES//4},1", sprite="./assets/sprites/npcs/plant.png",
            hostile=True),
        NPC(name='Goblin', hp=10, global_position="0,1", local_position=f"{view_cst.H_TILES//2},1", sprite="./assets/sprites/npcs/goblin.png",
            hostile=True),
        NPC(name='Skeleton', hp=12, global_position="0,1", local_position=f"{3*view_cst.H_TILES//4},1", sprite="./assets/sprites/npcs/skeleton.png",
            hostile=True),
    ]
    session.add_all(npcs)

    # Add 5 Items
    items = [
        Item(name="Dagger", description="A common iron dagger", global_position="0,0",
             local_position=f"{view_cst.H_TILES//2},{view_cst.V_TILES-1}", sprite="./assets/sprites/items/dagger.png"),
        Item(name="Shield", description="A common wooden shield", global_position="0,0",
             local_position=f"{view_cst.H_TILES//2},{view_cst.V_TILES-1}", sprite="./assets/sprites/items/shield.png"),
        Item(name="Health Potion", description="A weak health potion", global_position="0,0",
             local_position=f"{view_cst.H_TILES//2},{view_cst.V_TILES-1}", sprite="./assets/sprites/items/health_potion.png"),
        Item(name="Mana Potion", description="A weak mana potion", global_position="0,0",
             local_position=f"{view_cst.H_TILES//2},{view_cst.V_TILES-1}", sprite="./assets/sprites/items/mushroom.png"),
        Item(name="Mushroom", description="Good in an omelette", global_position="2,2",
             local_position=f"{view_cst.H_TILES//2},{view_cst.V_TILES//2}", sprite="./assets/sprites/items/mushroom.png"),
    ]
    session.add_all(items)

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