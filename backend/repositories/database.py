from .roomsRepository import RoomsRepository
from .usersRepository import UsersRepository
from .propositionsRepository import PropositionsRepository
from .votesRepository import VotesRepository
from pathlib import Path
import gc
from sqlmodel import create_engine, Session, SQLModel
from fastapi import Depends
from typing import Annotated
from datetime import datetime
import sqlite3

class Database:
    rooms: RoomsRepository = None
    users: UsersRepository = None
    propositions: PropositionsRepository = None
    votes: VotesRepository = None

    def __init__(self, session):
        self.rooms = RoomsRepository(session)
        self.users = UsersRepository(session)
        self.propositions = PropositionsRepository(session)
        self.votes = VotesRepository(session)

class DatabaseEngineConfig:
    db_file_name: str
    def __init__(self, db_file_name: str):
        self.db_file_name = db_file_name

    def get_db_url(self):
        return f"sqlite:///{self.db_file_name}"

engine = None
_config: DatabaseEngineConfig = None

def get_engine():
    if engine is None:
        raise Exception("DatabaseEngine is not initialized. Call DatabaseEngine(config) first.")

    return engine

def destroy():
    if engine is None:
        raise Exception("DatabaseEngine is not initialized.")
    
    engine.dispose()
    gc.collect()
    db_file = Path(_config.db_file_name)
    if db_file.exists():
        db_file.unlink()
    print(f"Database file {_config.db_file_name} has been deleted.")

def get_database():
    with Session(get_engine().engine) as session:
        yield Database(session)

def init_engine(config: DatabaseEngineConfig):
    connect_args = {"check_same_thread": False}
    global engine, _config
    sqlite3.register_adapter(datetime, lambda val: val.timestamp())
    sqlite3.register_converter("timestamp", lambda val: datetime.fromtimestamp(float(val)))

    engine = create_engine(config.get_db_url(), connect_args=connect_args)
    _config = config
    SQLModel.metadata.create_all(engine)


DatabaseDep = Annotated[Database, Depends(get_database)]

