import sqlite3
from sqlite3 import Error

def connect_to_db():
    try:
        connection = sqlite3.connect('article.db')
        connection.execute("""
                    CREATE TABLE IF NOT EXISTS article (
                        name TEXT NOT NULL,
                        date TEXT NOT NULL
                    );
                    """)

        return connection
    except Error as e:
        print(e)
        raise

def retrieve_article(connection, article):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM article WHERE name = ? and date = ?", (article['title'], article['date']))

    return cursor.fetchone()

def update_article(connection, article):
    connection.execute("DELETE FROM article")
    connection.commit()

    connection.execute("INSERT INTO article (name, date) VALUES (?, ?)", (article['title'], article['date']))
    connection.commit()

def close_connection(connection):
    connection.close()