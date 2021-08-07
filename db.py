# standard
import os
import sqlite3
# internal
import settings


def remove_old_db():
    if os.path.exists(settings.DATABASE_PATH):
        os.remove(settings.DATABASE_PATH)


def connection():
    first = not os.path.exists(settings.DATABASE_PATH)
    # create connection
    conn = sqlite3.connect(settings.DATABASE_PATH)
    # check for first run
    if first:
        # this is first run: lets create Categories table
        sql = """
            CREATE TABLE Categories(
                id          INTEGER         PRIMARY KEY     AUTOINCREMENT,
                name        VARCHAR(50)     NOT NULL,
                parent      INTEGER 
            )
        """
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.close()
        conn.commit()
    # return created connection
    return conn


def add_category(conn, name, parent):
    params = [name, parent]
    sql = """
        INSERT INTO Categories(name, parent)
        VALUES (?, ?)
    """
    cursor = conn.cursor()
    cursor.execute(sql, params)
    lastrowid = cursor.lastrowid
    cursor.close()
    return lastrowid


def all_categories(conn):
    sql = """SELECT * FROM Categories ORDER BY parent"""
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    return results
