from api import app
from fastapi.testclient import TestClient
from dotenv import load_dotenv
import os
import pytest
from repositories.db import Database
from pathlib import Path

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup():
    test_env_path = Path(__file__).parent / 'test.env'
    print(f"Loading environment variables from: {test_env_path}")
    load_dotenv(test_env_path, override=True)
    db_path = Path(__file__).parent / 'test.db'
    Database(db_path) 
    yield
    Database().destroy()
    
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Movie Night API!"}

def test_create_room():
    print("database file name:")
    print(os.getenv("DB_FILE_NAME"))
    response = client.post("/rooms", json={"name": "Test Create Room", "username": "Test User Create Room"})
    print(response.json())
    assert response.status_code == 201
    assert "room" in response.json()
    assert "user" in response.json()
    assert response.json()["room"]["name"] == "Test Create Room"
    assert response.json()["user"]["username"] == "Test User Create Room"

def test_create_room_invalid_data():
    response = client.post("/rooms", json={"name": "  ", "username": "  "})
    assert response.status_code == 400
    assert response.json() == {"detail": "Room name or username cannot be empty"}

    response = client.post("/rooms", json={"name": "ab", "username": "ab"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Room and user name must be at least 3 characters long"}

def test_get_room():
    create_response = client.post("/rooms", json={"name": "Test Room Get Room", "username": "Test User Get Room"})
    assert create_response.status_code == 201
    room_id = create_response.json()["room"]["id"]

    response = client.get(f"/rooms/Test%20Room%20Get%20Room")
    assert response.status_code == 200
    assert response.json()["room"]["id"] == room_id
    assert response.json()["room"]["name"] == "Test Room Get Room"
    assert len(response.json()["users"]) > 0 
    assert response.json()["users"][0][1] == "Test User Get Room"

def test_get_nonexistent_room():
    response = client.get("/rooms/Nonexistent+Room")
    assert response.status_code == 404
    assert response.json() == {"detail": "Room not found"}