from api import app
from fastapi.testclient import TestClient
from dotenv import load_dotenv
import pytest
from repositories.db import Database
from pathlib import Path

@pytest.fixture(scope="session", autouse=True)
def client():
    test_env_path = Path(__file__).parent / 'test.env'
    print(f"Loading environment variables from: {test_env_path}")
    load_dotenv(test_env_path, override=True)
    db_path = Path(__file__).parent / 'test.db'
    Database(db_path) 
    yield TestClient(app)
    Database().destroy()