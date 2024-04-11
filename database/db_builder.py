import psycopg2
import view.view_constants as view_cst

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

def create_tables(conn):
    cursor = conn.cursor()

    # Drop existing tables if they exist
    cursor.execute("DROP TABLE IF EXISTS characters CASCADE")
    cursor.execute("DROP TABLE IF EXISTS npcs CASCADE")
    cursor.execute("DROP TABLE IF EXISTS items CASCADE")

    # Create the characters table
    cursor.execute("""
        CREATE TABLE characters (
            id SERIAL PRIMARY KEY,
            name TEXT,
            hp INTEGER,
            global_position TEXT,
            local_position TEXT,
            sprite TEXT DEFAULT './assets/sprites/character.png'
        )
    """)

    # Create the npcs table
    cursor.execute("""
        CREATE TABLE npcs (
            id SERIAL PRIMARY KEY,
            name TEXT,
            hp INTEGER,
            global_position TEXT,
            local_position TEXT,
            sprite TEXT DEFAULT './assets/default.png',
            hostile BOOLEAN DEFAULT FALSE
        )
    """)

    # Create the items table
    cursor.execute("""
        CREATE TABLE items (
            id SERIAL PRIMARY KEY,
            name TEXT,
            description TEXT,
            global_position TEXT,
            local_position TEXT,
            sprite TEXT DEFAULT './assets/default.png',
            in_world BOOLEAN DEFAULT FALSE
        )
    """)

    conn.commit()
    print("Tables created successfully")

def populate_tables(conn):
    cursor = conn.cursor()

    # Insert character
    cursor.execute("""
        INSERT INTO characters (name, hp, global_position, local_position, sprite)
        VALUES (%s, %s, %s, %s, %s)
    """, ('Gary', 16, '0,0', f"{view_cst.H_TILES//2},{view_cst.V_TILES-1}", './assets/sprites/character/character.png'))

    # Insert NPCs
    npcs = [
        ('Blacksmith', 50, '0,0', f"{view_cst.H_TILES},{view_cst.V_TILES//2}", './assets/sprites/npcs/blacksmith.png', False),
        ('Elder', 50, '0,0', f"{view_cst.H_TILES//3},1", './assets/sprites/npcs/elder.png', False),
        ('Enchantress', 20, '0,0', f"1,{view_cst.V_TILES//2}", './assets/sprites/npcs/enchantress.png', False),
        ('Robot', 1000, '0,0', f"{2*view_cst.H_TILES//3},1", './assets/sprites/npcs/robot.png', False),
        ('Plant', 8, '0,1', f"{view_cst.H_TILES//4},1", './assets/sprites/npcs/plant.png', True),
        ('Goblin', 10, '0,1', f"{view_cst.H_TILES//2},1", './assets/sprites/npcs/goblin.png', True),
        ('Skeleton', 12, '0,1', f"{3*view_cst.H_TILES//4},1", './assets/sprites/npcs/skeleton.png', True),
    ]
    for npc in npcs:
        cursor.execute("""
            INSERT INTO npcs (name, hp, global_position, local_position, sprite, hostile)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, npc)

    # Insert items
    items = [
        ('Dagger', "A common iron dagger", '0,0', f"{view_cst.H_TILES//2},{view_cst.V_TILES-1}", './assets/sprites/items/dagger.png', False),
        ('Shield', "A common wooden shield", '0,0', f"{view_cst.H_TILES//2},{view_cst.V_TILES-1}", './assets/sprites/items/shield.png', False),
        ('Health Potion', "A weak health potion", '0,0', f"{view_cst.H_TILES//2},{view_cst.V_TILES-1}", './assets/sprites/items/health_potion.png', False),
        ('Mana Potion', "A weak mana potion", '0,0', f"{view_cst.H_TILES//2},{view_cst.V_TILES-1}", './assets/sprites/items/mana_potion.png', False),
        ('Mushroom', "Good in an omelette", '1,0', f"{view_cst.H_TILES//2},{view_cst.V_TILES//2}", './assets/sprites/items/mushroom.png', True),
        ('Throwing daggers', "Make sure to grab them by the correct end.", '1,0', f"{view_cst.H_TILES},{view_cst.V_TILES // 2}",'./assets/sprites/items/throwing_daggers.png', True),
    ]
    for item in items:
        cursor.execute("""
            INSERT INTO items (name, description, global_position, local_position, sprite, in_world)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, item)

    conn.commit()
    print("Tables populated successfully")

if __name__ == "__main__":
    conn = connect_to_db()
    create_tables(conn)
    populate_tables(conn)
    conn.close()









# import psycopg2
# from sqlalchemy import update
# from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship
# # from sqlalchemy.orm import declared_attr
# # from sqlalchemy.sql.schema import Table
# import view.view_constants as view_cst
#
# engine = create_engine('postgresql+psycopg2://rani:ranidb@localhost/llmgame')
# Base = declarative_base()
#
# #TODO: will need methods to update some attributes of an object
# #TODO: How to handle quests and objective. May not need to store objectives since th
#
# class Character(Base):
#     __tablename__ = 'characters'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     hp = Column(Integer)
#     global_position = Column(String)  #"x,y"
#     local_position = Column(String)  #"x,y"
#     sprite = Column(String, default="./assets/sprites/character.png")
#
# class NPC(Base):
#     __tablename__ = 'npcs'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     hp = Column(Integer)
#     global_position = Column(String)  #"x,y"
#     local_position = Column(String)  #"x,y
#     sprite = Column(String, default="./assets/default.png")
#     hostile = Column(Boolean, default=False)
#
# class Item(Base):
#     __tablename__ = 'items'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     description = Column(String)
#     global_position = Column(String)  #"x,y"
#     local_position = Column(String)  #"x,y"
#     sprite = Column(String, default="./assets/default.png")
#
# def load_database():
#     print(f"Adding instances to the database")
#     # First, create the database schema
#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)
#
#     # Create a session
#     Session = sessionmaker(bind=engine)
#     session = Session()
#
#     character = Character(name='Gary', hp=16, global_position="0,0", local_position=f"{view_cst.H_TILES//2},{view_cst.V_TILES-1}",
#                           sprite="./assets/sprites/character/character.png")
#     session.add(character)
#
#     # Add 5 NPCs (2 friendly, 3 hostile)
#     npcs = [
#         NPC(name='Elder', hp=1000, global_position="0,0", local_position=f"{view_cst.H_TILES//3},1", sprite="./assets/sprites/npcs/elder.png",
#             hostile=False),
#         NPC(name='Robot', hp=10000, global_position="0,0", local_position=f"{2*view_cst.H_TILES//3},1", sprite="./assets/sprites/npcs/robot.png",
#             hostile=False),
#         NPC(name='Plant', hp=8, global_position="0,1", local_position=f"{view_cst.H_TILES//4},1", sprite="./assets/sprites/npcs/plant.png",
#             hostile=True),
#         NPC(name='Goblin', hp=10, global_position="0,1", local_position=f"{view_cst.H_TILES//2},1", sprite="./assets/sprites/npcs/goblin.png",
#             hostile=True),
#         NPC(name='Skeleton', hp=12, global_position="0,1", local_position=f"{3*view_cst.H_TILES//4},1", sprite="./assets/sprites/npcs/skeleton.png",
#             hostile=True),
#     ]
#     session.add_all(npcs)
#
#     # Add 5 Items
#     items = [
#         Item(name="Dagger", description="A common iron dagger", global_position="0,0",
#              local_position=f"{view_cst.H_TILES//2},{view_cst.V_TILES-1}", sprite="./assets/sprites/items/dagger.png"),
#         Item(name="Shield", description="A common wooden shield", global_position="0,0",
#              local_position=f"{view_cst.H_TILES//2},{view_cst.V_TILES-1}", sprite="./assets/sprites/items/shield.png"),
#         Item(name="Health Potion", description="A weak health potion", global_position="0,0",
#              local_position=f"{view_cst.H_TILES//2},{view_cst.V_TILES-1}", sprite="./assets/sprites/items/health_potion.png"),
#         Item(name="Mana Potion", description="A weak mana potion", global_position="0,0",
#              local_position=f"{view_cst.H_TILES//2},{view_cst.V_TILES-1}", sprite="./assets/sprites/items/mushroom.png"),
#         Item(name="Mushroom", description="Good in an omelette", global_position="1,0",
#              local_position=f"{view_cst.H_TILES//2},{view_cst.V_TILES//2}", sprite="./assets/sprites/items/mushroom.png"),
#     ]
#     session.add_all(items)
#
#     # Commit everything to the database
#     session.commit()
#
#     # Close the session
#     session.close()
#
# def connect_to_db():
#     try:
#         conn = psycopg2.connect(
#             dbname="llmgame",
#             user="rani",  # replace with your PostgreSQL username
#             password="ranidb",  # replace with your password
#             host="localhost"
#         )
#     except psycopg2.Error as e:
#         print("Unable to connect to the database")
#         print(e)
#     else:
#         print("Connected to the database")
#         return conn
# def create_table(conn):
#     cursor = conn.cursor()
#     sql_create_table = """
#     CREATE TABLE IF NOT EXISTS new_table (
#         id SERIAL PRIMARY KEY,
#         name TEXT NOT NULL,
#         email TEXT NOT NULL
#     )
#     """
#     try:
#         cursor.execute(sql_create_table)
#     except psycopg2.Error as e:
#         print("Error creating table")
#         print(e)
#     else:
#         print("Table created successfully")
#         conn.commit()
#
# if __name__ == "__main__":
#     load_database()
#     # # Querying characters
#     # hero = session.query(Character).filter_by(name="Hero").first()
#     # print(hero.name)
#
#
#     # conn = connect_to_db()
#     # create_table(conn)
#     # conn.close()