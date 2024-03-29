import psycopg2



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
    conn = connect_to_db()
    create_table(conn)
    conn.close()