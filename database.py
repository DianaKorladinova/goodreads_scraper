import sqlite3
from sqlite3 import Error


def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(r"/var/lib/db/pythonsqlite.db")
        sql_statement = """
        CREATE TABLE IF NOT EXISTS Books(id INTEGER PRIMARY KEY,
                                Title VARCHAR(255),
                                Author VARCHAR(255),
                                Genre VARCHAR(255),
                                Average VARCHAR(255),
                                Ratings VARCHAR(255),
                                Url VARCHAR(255));
        
        """
        cursor = conn.cursor()
        cursor.execute(sql_statement)
        return conn
    except Error as e:
        print(e)


def insert_stuff(title, author, genre, average, ratings, url, connection):
    params = (title, author, genre, average, ratings, url)
    sql_stat = '''
    INSERT INTO Books (Title, Author, Genre, Average, Ratings, Url) VALUES (?,?,?,?,?,?);
    '''
    print(params)
    connection.cursor().execute(sql_stat, params)
    connection.commit()
