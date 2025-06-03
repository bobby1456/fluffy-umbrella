from contextlib import asynccontextmanager

from fastapi import FastAPI
from repositories import database
from api import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    config = database.DatabaseEngineConfig(db_file_name="database.db")
    database.init_engine(config)


app = FastAPI(lifespan=lifespan)
app.include_router(router, tags=["rooms"])