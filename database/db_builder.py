import psycopg2

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
