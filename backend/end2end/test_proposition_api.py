from api import app
from fastapi.testclient import TestClient
from dotenv import load_dotenv
import os
import pytest
from repositories.db import Database
from pathlib import Path

@pytest.fixture(scope="module")
def room_and_user_setup(client):
    response = client.post("/rooms", json={"name": "Test Room Proposition", "username": "Test User Proposition"})
    assert response.status_code == 201
    return response.json()["room"]["id"], response.json()["users"][0]["id"]

def test_create_proposition(client, room_and_user_setup):
    _, user_id = room_and_user_setup
    response = client.post(f"/users/{user_id}/propositions", json={"film_name": "Inception"})
    assert response.status_code == 201
    assert response.json()["film_name"] == "Inception"
    assert response.json()["proposition_id"] == user_id

def test_create_proposition_invalid_data(client, room_and_user_setup):
    _, user_id = room_and_user_setup
    response = client.post(f"/users/{user_id}/propositions", json={"film_name": "  "})
    assert response.status_code == 400
    assert response.json()["detail"] is not None

    response = client.post(f"/users/{user_id}/propositions", json={})
    assert response.status_code == 422
    assert response.json()["detail"] is not None