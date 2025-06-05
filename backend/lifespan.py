from contextlib import asynccontextmanager

from fastapi import FastAPI

from repositories import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = database.DatabaseEngineConfig(db_file_name="database.db")
    database.init_engine(config)
    yield
    database.close()

