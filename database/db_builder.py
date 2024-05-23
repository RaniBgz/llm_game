import psycopg2
import view.view_constants as view_cst
import json
import database.data_constants as data_cst
from langchain_openai.embeddings import OpenAIEmbeddings
from sentence_transformers import SentenceTransformer

H = view_cst.H_TILES
V = view_cst.V_TILES

class DBBuilder():
    def __init__(self):
        self.conn = self.connect_to_db()
        self.embedding_model = None


    def embed_text(self, text):
        return self.embedding_model.encode(text, convert_to_tensor=True)

    def embed_text_to_list(self, text):
        if self.embedding_model is None:
            self.embedding_model = SentenceTransformer('all-miniLM-L6-v2')
        return self.embedding_model.encode(text).tolist()

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

    def ensure_pgvector_extension(self):
        cursor = self.conn.cursor()
        try:
            # Attempt to create the extension (does nothing if already exists)
            cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            self.conn.commit()
            print("pgvector extension ensured.")
        except psycopg2.Error as e:
            print("Error ensuring pgvector extension:", e)
        finally:
            cursor.close()

    def create_tables(self):
        cursor = self.conn.cursor()

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

        self.conn.commit()
        print("Tables created successfully")

    def add_vector_column(self, table_name, vector_dim=data_cst.EMBEDDING_DIM):
        cursor = self.conn.cursor()
        try:
            # SQL command to add a vector column
            cursor.execute(f"""
            ALTER TABLE {table_name} 
            ADD COLUMN IF NOT EXISTS embedding vector({vector_dim});
            """)
            self.conn.commit()
            print(f"Vector column added to {table_name}.")
        except psycopg2.Error as e:
            print(f"Error adding vector column to {table_name}:", e)
        finally:
            cursor.close()

    def remove_vector_column(self, table_name):
        cursor = self.conn.cursor()
        try:
            # SQL command to remove the vector column
            cursor.execute(f"""
            ALTER TABLE {table_name} 
            DROP COLUMN IF EXISTS embedding;
            """)
            self.conn.commit()
            print(f"Vector column removed from {table_name}.")
        except psycopg2.Error as e:
            print(f"Error removing vector column from {table_name}:", e)
        finally:
            cursor.close()

#TODO: When the DB grows, think about using fetchone instead of fetchall
#TODO: Properly define process to add an entity to the DB and build its vector at the same time
    def build_character_vectors(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
            SELECT id, name
            FROM characters
            WHERE embedding IS NULL;
            """)
            rows = cursor.fetchall()
            for row in rows:
                npc_id, npc_name = row  # Unpack the id and name directly

                # Generate the embedding for the name only
                row_vector = self.embed_text_to_list(npc_name)

                cursor.execute("""
                UPDATE characters SET embedding = %s WHERE id = %s;
                """, (row_vector, npc_id))
            self.conn.commit()
        except psycopg2.Error as e:
            print("Error retrieving Character data:", e)
        finally:
            cursor.close()

    def build_npcs_vectors(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
            SELECT id, name
            FROM npcs 
            WHERE embedding IS NULL;
            """)
            rows = cursor.fetchall()
            for row in rows:
                npc_id, npc_name = row  # Unpack the id and name directly

                # Generate the embedding for the name only
                row_vector = self.embed_text_to_list(npc_name)

                cursor.execute("""
                UPDATE npcs SET embedding = %s WHERE id = %s;
                """, (row_vector, npc_id))
            self.conn.commit()
        except psycopg2.Error as e:
            print("Error retrieving NPCs data:", e)
        finally:
            cursor.close()

    def build_items_vectors(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
            SELECT id, name
            FROM items 
            WHERE embedding IS NULL;
            """)
            rows = cursor.fetchall()
            for row in rows:
                npc_id, npc_name = row  # Unpack the id and name directly

                # Generate the embedding for the name only
                row_vector = self.embed_text_to_list(npc_name)

                cursor.execute("""
                UPDATE items SET embedding = %s WHERE id = %s;
                """, (row_vector, npc_id))
            self.conn.commit()
        except psycopg2.Error as e:
            print("Error retrieving Items data:", e)
        finally:
            cursor.close()

    def verify_vectors(self, table_name):
        cursor = self.conn.cursor()
        try:
            # Query to check a few rows
            cursor.execute(f"SELECT id, embedding FROM {table_name} WHERE embedding IS NOT NULL LIMIT 5;")
            rows = cursor.fetchall()
            for row in rows:
                print(f"ID: {row[0]}, Embedding: {row[1][:10]}...")  # Print the first 10 elements of the embedding
        except psycopg2.Error as e:
            print(f"Error checking embeddings in {table_name}:", e)
        finally:
            cursor.close()

    def populate_tables(self, conn):
        cursor = conn.cursor()

        # Insert character
        cursor.execute("""
            INSERT INTO characters (name, hp, global_position, local_position, sprite)
            VALUES (%s, %s, %s, %s, %s)
        """, ('Gary', 16, '3,3', f"{H//2},{V-1}", './assets/sprites/character/character.png'))

        # Insert NPCs
        npcs = [
            ('Blacksmith', 50, False, '3,3', f"{H},{V//2}", './assets/sprites/npcs/blacksmith.png', False),
            ('Elder', 50, False, '3,3', f"{H//2 - 1},1", './assets/sprites/npcs/elder.png', False),
            ('Enchantress', 20, False, '3,3', f"1,{V//2}", './assets/sprites/npcs/enchantress.png', False),
            ('Echo', 1000, True, '3,3', f"{2*H//3},1", './assets/sprites/npcs/robot.png', False),
            ('Plant', 8, False, '3,4', f"{H//4},1", './assets/sprites/npcs/plant.png', True),
            ('Goblin', 10, False, '3,4', f"{H//2},1", './assets/sprites/npcs/goblin.png', True),
            ('Skeleton', 12, False, '3,4', f"{3*H//4},1", './assets/sprites/npcs/skeleton.png', True),
        ]
        for npc in npcs:
            cursor.execute("""
                INSERT INTO npcs (name, hp, robot, global_position, local_position, sprite, hostile)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, npc)

        # Insert items
        items = [
            ('Iron Dagger', "A common iron dagger", '3,3', f"{H//2},{V-1}", './assets/sprites/items/iron_dagger.png', False),
            ('Wooden Shield', "A common wooden shield", '3,3', f"{H//2},{V-1}", './assets/sprites/items/wooden_shield.png', False),
            ('Small Health Potion', "A weak health potion", '3,3', f"{H//2},{V-1}", './assets/sprites/items/small_health_potion.png', False),
            ('Small Mana Potion', "A weak mana potion", '3,3', f"{H//2},{V-1}", './assets/sprites/items/small_mana_potion.png', False),
            ('Mushroom', "Good in an omelette", '4,3', f"{H//2},{V//2}", './assets/sprites/items/mushroom.png', True),
            ('Throwing daggers', "Make sure to grab them by the correct end.", '4,3', f"{H},{V//2}",'./assets/sprites/items/throwing_daggers.png', True),
        ]
        for item in items:
            cursor.execute("""
                INSERT INTO items (name, description, global_position, local_position, sprite, in_world)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, item)

        conn.commit()
        print("Tables populated successfully")

    def clear_all_tables(self):
        cursor = self.conn.cursor()
        try:
            # Delete all entries from each table
            cursor.execute("DELETE FROM characters;")
            cursor.execute("DELETE FROM npcs;")
            cursor.execute("DELETE FROM items;")
            self.conn.commit()
            print("All tables cleared successfully.")
        except psycopg2.Error as e:
            print("Error clearing tables:", e)
        finally:
            cursor.close()

    def add_npc(self, name, hp, robot, global_position, local_position, sprite, hostile):
        cursor = self.conn.cursor()
        try:
            npc_vector = self.embed_text_to_list(name)
            cursor.execute("""
                INSERT INTO npcs (name, hp, robot, global_position, local_position, sprite, hostile, embedding)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, hp, robot, global_position, local_position, sprite, hostile, npc_vector))
            self.conn.commit()
            print("NPC added successfully")
        except psycopg2.Error as e:
            print("Error adding NPC:", e)
        finally:
            cursor.close()

    def add_item(self, name, description, global_position, local_position, sprite, in_world):
        cursor = self.conn.cursor()
        try:
            item_vector = self.embed_text_to_list(name)
            cursor.execute("""
                INSERT INTO items (name, description, global_position, local_position, sprite, in_world, embedding)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (name, description, global_position, local_position, sprite, in_world, item_vector))
            self.conn.commit()
            print("Item added successfully")
        except psycopg2.Error as e:
            print("Error adding item:", e)
        finally:
            cursor.close()

    def close_connection(self):
        self.conn.close()

if __name__ == "__main__":
    db_builder = DBBuilder()
    # db_builder.clear_all_tables()
    # db_builder.populate_tables(db_builder.conn)
    # db_builder.build_character_vectors()
    # db_builder.verify_vectors('characters')
    # db_builder.build_npcs_vectors()
    # db_builder.verify_vectors('npcs')
    # db_builder.build_items_vectors()
    # db_builder.verify_vectors('items')

    db_builder.add_npc('New NPC', 30, False, '1,1', '2,2', './assets/sprites/npcs/new_npc.png', False)
    db_builder.add_item('New Item', 'A mysterious new item', '1,1', '2,2', './assets/sprites/items/new_item.png', True)

    # db_builder.remove_vector_column('npcs')
    # db_builder.remove_vector_column('items')
    # db_builder.remove_vector_column('characters')

    # db_builder.add_vector_column('npcs', vector_dim=data_cst.EMBEDDING_DIM)
    # db_builder.add_vector_column('items', vector_dim=data_cst.EMBEDDING_DIM)
    # db_builder.add_vector_column('characters', vector_dim=data_cst.EMBEDDING_DIM)


    db_builder.close_connection()

