import psycopg2
import view.view_constants as view_cst
import json
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai.services.open_ai_text_embedding import OpenAITextEmbedding
from semantic_kernel.core_plugins.text_memory_plugin import TextMemoryPlugin
from semantic_kernel.kernel import Kernel
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory
from semantic_kernel.memory.volatile_memory_store import VolatileMemoryStore
import database.data_constants as data_cst
from langchain_openai.embeddings import OpenAIEmbeddings
from sentence_transformers import SentenceTransformer, util

#https://github.com/microsoft/semantic-kernel/blob/main/python/notebooks/06-memory-and-embeddings.ipynb
#https://platform.openai.com/docs/models/embeddings


#1,536

class DBBuilder():
    def __init__(self):
        self.conn = self.connect_to_db()
        self.embedding_model = SentenceTransformer('all-miniLM-L6-v2')


    def embed_text(self, text):
        return self.embedding_model.encode(text, convert_to_tensor=True)

    def embed_text_to_list(self, text):
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

    def add_vector_column(self, table_name, vector_dim=128):
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

#TODO: Add a method to create the embedding
    def build_character_vector(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
            SELECT id, name, hp, global_position, local_position, sprite 
            FROM characters 
            WHERE embedding IS NULL;
            """)
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            for row in rows:
                row_dict = dict(zip(column_names, row))
                row_json = json.dumps(row_dict)
                row_vector = self.embed_text_to_list(row_json)
                cursor.execute("""
                UPDATE characters SET embedding = %s WHERE id = %s;
                """, (row_vector, row_dict['id']))
            self.conn.commit()
        except psycopg2.Error as e:
            print("Error retrieving characters data:", e)
        finally:
            cursor.close()

    def build_npcs_vector(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
            SELECT id, name, hp, robot, global_position, local_position, sprite, hostile 
            FROM npcs 
            WHERE embedding IS NULL;
            """)
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            for row in rows:
                row_dict = dict(zip(column_names, row))
                row_json = json.dumps(row_dict)
                row_vector = self.embed_text_to_list(row_json)
                cursor.execute("""
                UPDATE npcs SET embedding = %s WHERE id = %s;
                """, (row_vector, row_dict['id']))
            self.conn.commit()
        except psycopg2.Error as e:
            print("Error retrieving NPCs data:", e)
        finally:
            cursor.close()

    def build_items_vector(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute("""
            SELECT id, name, description, global_position, local_position, sprite, in_world 
            FROM items 
            WHERE embedding IS NULL;
            """)
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            for row in rows:
                row_dict = dict(zip(column_names, row))
                row_json = json.dumps(row_dict)
                row_vector = self.embed_text_to_list(row_json)
                cursor.execute("""
                UPDATE items SET embedding = %s WHERE id = %s;
                """, (row_vector, row_dict['id']))
            self.conn.commit()
        except psycopg2.Error as e:
            print("Error retrieving items data:", e)
        finally:
            cursor.close()

    def populate_tables(self, conn):
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

    def close_connection(self):
        self.conn.close()

if __name__ == "__main__":
    db_builder = DBBuilder()
    # db_builder.remove_vector_column('npcs')
    # db_builder.remove_vector_column('items')
    # db_builder.remove_vector_column('characters')
    db_builder.add_vector_column('npcs', vector_dim=data_cst.EMBEDDING_DIM)
    db_builder.add_vector_column('items', vector_dim=data_cst.EMBEDDING_DIM)
    db_builder.add_vector_column('characters', vector_dim=data_cst.EMBEDDING_DIM)
    db_builder.close_connection()

