import os

SQL_LITE_DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'sql_lite_databases', 'quotes.db')

SQL_AUTHOR_TABLE_NAME = 'author'
SQL_QUOTE_TABLE_NAME = 'quote'

SQL_CREATE_AUTHOR_TABLE_QUERY = f"""
    CREATE TABLE IF NOT EXISTS {SQL_AUTHOR_TABLE_NAME} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        surname TEXT,
        born_date INTEGER,
        born_location TEXT,
        description TEXT
    );
"""

SQL_CREATE_QUOTE_TABLE_QUERY = f"""
    CREATE TABLE IF NOT EXISTS {SQL_QUOTE_TABLE_NAME} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        tags TEXT,
        author_id INTEGER,
        FOREIGN KEY (author_id) REFERENCES author (id) ON DELETE CASCADE
    );
"""