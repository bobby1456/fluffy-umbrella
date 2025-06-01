from fastapi.testclient import TestClient
from fastapi import FastAPI
from api import router as api_router
import pytest
from repositories import database
from pathlib import Path

@pytest.fixture(scope="session", autouse=True)
def client():
    db_config = database.DatabaseEngineConfig(db_file_name="test_database.db")
    database.init_engine(db_config)
    app = FastAPI()
    app.include_router(api_router)
    yield TestClient(app)
    database.destroy()
