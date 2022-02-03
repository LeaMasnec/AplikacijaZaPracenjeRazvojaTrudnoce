DB_HOST = "localhost"
DB_NAME = "trudnoca"
DB_USER = "postgres"
DB_PASS = "0000"


import psycopg2
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

def connect_db():
    if (conn) :
        print("Ostvarena konekcija!")
    else:
        print("Problem u spajanju!")

def close_db():
    conn.close()