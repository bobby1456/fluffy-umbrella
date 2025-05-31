import sqlite3
from sqlite3 import Connection
import threading
import os
from .room import RoomsRepository
from .user import UsersRepository
from .proposition import PropositionsRepository
from .vote import VotesRepository
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
    propositions: PropositionsRepository = None
    votes: VotesRepository = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    print("No existing instance found, creating a new one.")
                    cls._instance = super(Database, cls).__new__(cls)
                    cls._instance.init_instance(*args, **kwargs)

        return cls._instance
    
    def init_instance(self, db_path = None):
        self._db_path = db_path if db_path is not None else Path(__file__).parent / os.getenv('DB_FILE_NAME')
        self._conn = sqlite3.connect(self._db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        print(f"Database connection established to {self._db_path}")

        sql_file = Path(__file__).parent.parent / 'db.sql'
        if sql_file.exists():
            with sql_file.open() as f:
                sql_script = f.read()
                self._conn.executescript(sql_script)
                self._conn.commit()
        self.rooms = RoomsRepository(self._conn)
        self.users = UsersRepository(self._conn)
        self.propositions = PropositionsRepository(self._conn)
        self.votes = VotesRepository(self._conn)
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
                print(f"Database file {self._db_path} deleted.")
            else:
                raise FileNotFoundError(f"Database file {self._db_path} does not exist.")
            
            self._instance = None
