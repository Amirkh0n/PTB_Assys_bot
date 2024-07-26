import sqlite3
from abc import ABC, abstractmethod
from contextlib import closing


class BaseCRUD(ABC):
    def __init__(self, database_path, table_name):
        self.database_path = database_path
        self.table_name = table_name

    
    def get_connection(self):
        return closing(sqlite3.connect(self.database_path))

    def migrate(self):
      with self.get_connection() as connection:
        cursor = connection.cursor()
        # Jadval yaratish
        queries = [
            '''
            CREATE TABLE IF NOT EXISTS users(
              user_id INTEGER PRIMARY KEY NOT NULL,
              name TEXT
            );
            ''',
            '''
            CREATE TABLE IF NOT EXISTS tests (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              title TEXT NOT NULL,
              description TEXT, 
              filename TEXT,
              user_id INTEGER NOT NULL,
              FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
            '''
        ]

        for query in queries:
            cursor.execute(query)
        
        connection.commit()
        print('Database created!')
    
    def insert(self, **kwargs):
        while True: 
            try:
              with self.get_connection() as connection:
                cursor = connection.cursor()
                columns = ', '.join(kwargs.keys())
                placeholders = ', '.join('?' for _ in kwargs)
                query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
                cursor.execute(query, tuple(kwargs.values()))
                connection.commit()
                return cursor.lastrowid
            except sqlite3.OperationalError:
                self.migrate()

    def get_all(self):
        while True: 
            try:
              with self.get_connection() as connection:
                cursor = connection.cursor()
                query = f"SELECT * FROM {self.table_name}"
                cursor.execute(query)
                return cursor.fetchall()
            except sqlite3.OperationalError:
                self.migrate()
        
    def get(self, id, id_column="id",  all=False):
        while True:
            try:
              with self.get_connection() as connection:
                cursor = connection.cursor()
                query = f"SELECT * FROM {self.table_name} WHERE {id_column}=?"
                cursor.execute(query, (id,))
                if all:
                    return cursor.fetchall()
                return cursor.fetchone()
            except sqlite3.OperationalError:
                self.migrate()

    def get_all_user_id(self):
        while True: 
            try:
              with self.get_connection() as connection:
                cursor = connection.cursor()
                query = f"SELECT user_id FROM users"
                cursor.execute(query)
                return [user[0] for user in cursor.fetchall()]
            except sqlite3.OperationalError:
                self.migrate()
        
    def update(self, id, id_column="id", **kwargs):
        while True: 
            try:
              with self.get_connection() as connection:
                cursor = connection.cursor()
                columns = ', '.join(f"{key}=?" for key in kwargs)
                query = f"UPDATE {self.table_name} SET {columns} WHERE {id_column}=?"
                cursor.execute(query, (*kwargs.values(), id))
                connection.commit()
                return
            except sqlite3.OperationalError:
                self.migrate()

    def delete(self, id, id_column="id"):
        while True: 
            try:
              with self.get_connection() as connection:
                cursor = connection.cursor()
                query = f"DELETE FROM {self.table_name} WHERE {id_column}=?"
                cursor.execute(query, (id,))
                connection.commit()
                return 
            except sqlite3.OperationalError:
                self.migrate()
    
    def get_all_tests(self, user_id):
        while True: 
            try:
                with self.get_connection() as connection:
                    cursor = connection.cursor()
                    query = "SELECT * FROM tests WHERE user_id = ?;"
                    cursor.execute(query, (user_id,))
            
                    return [{'id': survey[0], 'title': survey[1], 'description': survey[2], 'user_id': survey[3]} for survey in cursor.fetchall()]
            except sqlite3.OperationalError:
                    self.migrate()
                    
