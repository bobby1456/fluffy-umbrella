import sqlite3
from sqlite3 import Connection
import threading
import os
from .room import RoomsRepository
from .user import UsersRepository
from pathlib import Path
import gc



class Database:
    _instance = None
    _db_path:Path = None
    _lock = threading.Lock()
    _conn_lock = threading.Lock()
    _conn:Connection  = None

    users: UsersRepository = None
    rooms: RoomsRepository = None

    def __new__(cls, db_path=None):
        print("Creating or retrieving the singleton Database instance...")
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Database, cls).__new__(cls)
                    
        return cls._instance
    
    def __init__(self, db_path = None):
        self._db_path = db_path if db_path is not None else Path(__file__).parent / os.getenv('DB_FILE_NAME')
        self._instance._conn = sqlite3.connect(self._db_path, check_same_thread=False)
        print(f"Database connection established to {self._db_path}")

        sql_file = Path(__file__).parent.parent / 'db.sql'
        if sql_file.exists():
            with sql_file.open() as f:
                sql_script = f.read()
                self._instance._conn.executescript(sql_script)
                self._instance._conn.commit()
        self.rooms = RoomsRepository(self._instance._conn)
        self.users = UsersRepository(self._instance._conn)
        sql_file = Path(__file__).parent / 'db.sql'
        if os.path.exists(sql_file):
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_script = f.read()
                self._conn.executescript(sql_script)
                self._conn.commit()
        else:
            raise FileNotFoundError(f"SQL file {sql_file} does not exist. Please ensure the database schema is set up correctly.")


    def destroy(self):
        print("Destroying database instance...")
        print(f"Database path: {self._db_path}")
        print(f"database instance path ")
        with self._lock:
            
            if self._conn:
                self._conn.close()
                self._conn = None
                print("Database connection closed.")

            if self._db_path is not None and self._db_path.exists():
                gc.collect()
                self._db_path.unlink()
            else:
                raise FileNotFoundError(f"Database file {self._db_path} does not exist.")
            
            self._instance = None



    def create_proposition(self, room_id, user_id, film_name):
        with self._conn_lock:
            cursor = self._conn.cursor()
            cursor.execute(
                "INSERT INTO proposition (room_id, user_id, film_name) VALUES (?, ?, ?)",
                (room_id, user_id, film_name)
            )
            self._conn.commit()
            return cursor.lastrowid

    def get_proposition(self, proposition_id):
        with self._conn_lock:
            cursor = self._conn.cursor()
            cursor.execute("SELECT * FROM proposition WHERE id = ?", (proposition_id,))
            return cursor.fetchone()

    def update_proposition(self, proposition_id, film_name=None):
        with self._conn_lock:
            cursor = self._conn.cursor()
            if film_name:
                cursor.execute(
                    "UPDATE proposition SET film_name = ? WHERE id = ?",
                    (film_name, proposition_id)
                )
                self._conn.commit()

    def delete_proposition(self, proposition_id):
        with self._conn_lock:
            cursor = self._conn.cursor()
            cursor.execute("DELETE FROM proposition WHERE id = ?", (proposition_id,))
            self._conn.commit()

    def create_vote(self, proposition_id, user_id, vote_type):
        with self._conn_lock:
            cursor = self._conn.cursor()
            cursor.execute(
                "INSERT INTO vote (proposition_id, user_id, vote_type) VALUES (?, ?, ?)",
                (proposition_id, user_id, vote_type)
            )
            self._conn.commit()
            return cursor.lastrowid

    def get_vote(self, vote_id):
        with self._conn_lock:
            cursor = self._conn.cursor()
            cursor.execute("SELECT * FROM vote WHERE id = ?", (vote_id,))
            return cursor.fetchone()

    def update_vote(self, vote_id, vote_type):
        with self._conn_lock:
            cursor = self._conn.cursor()
            cursor.execute(
                "UPDATE vote SET vote_type = ? WHERE id = ?",
                (vote_type, vote_id)
            )
            self._conn.commit()

    def delete_vote(self, vote_id):
        with self._conn_lock:
            cursor = self._conn.cursor()
            cursor.execute("DELETE FROM vote WHERE id = ?", (vote_id,))
            self._conn.commit()