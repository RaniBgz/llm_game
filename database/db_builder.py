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
            robot BOOLEAN DEFAULT FALSE,
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
        ('Blacksmith', 50, False, '0,0', f"{view_cst.H_TILES},{view_cst.V_TILES//2}", './assets/sprites/npcs/blacksmith.png', False),
        ('Elder', 50, False, '0,0', f"{view_cst.H_TILES//3},1", './assets/sprites/npcs/elder.png', False),
        ('Enchantress', 20, False, '0,0', f"1,{view_cst.V_TILES//2}", './assets/sprites/npcs/enchantress.png', False),
        ('Echo', 1000, True, '0,0', f"{2*view_cst.H_TILES//3},1", './assets/sprites/npcs/robot.png', False),
        ('Plant', 8, False, '0,1', f"{view_cst.H_TILES//4},1", './assets/sprites/npcs/plant.png', True),
        ('Goblin', 10, False, '0,1', f"{view_cst.H_TILES//2},1", './assets/sprites/npcs/goblin.png', True),
        ('Skeleton', 12, False, '0,1', f"{3*view_cst.H_TILES//4},1", './assets/sprites/npcs/skeleton.png', True),
    ]
    for npc in npcs:
        cursor.execute("""
            INSERT INTO npcs (name, hp, robot, global_position, local_position, sprite, hostile)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
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
