import psycopg2
def connect_database():
    con = psycopg2.connect(
        dbname='postgres',
        user = 'user',
        host = 'localhost',
        password = 'password')
    cur = con.cursor()
    cur.execute('CREATE DATABASE database')
    print("Database opened successfully")
    con.close()

connect_database()