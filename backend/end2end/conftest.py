from typing import Generator
from fastapi.testclient import TestClient
from fastapi import FastAPI
from api import router as api_router
from pytest import fixture, FixtureRequest
from repositories import database
from api import router

def create_test_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router, tags=["rooms"])
    return app

@fixture(scope="session", autouse=True)
def client()-> Generator[TestClient]:
    db_config = database.DatabaseEngineConfig(db_file_name="test_database.db")
    database.init_engine(db_config)

    app = create_test_app()
    yield TestClient(app)
    database.destroy()

@fixture(scope="function")
def test_suffix(request:FixtureRequest):
    return request.function.__name__.replace("test_", "").replace("_", " ").title()

@fixture(scope="function")
def room(client, test_suffix:str):
    response = client.post("/rooms", json={"name": f"Test Room {test_suffix}", "username": f"Test User {test_suffix}"})
    if response.status_code != 201:
        raise Exception(f"Failed to create room: {response.json()}")
    return response.json()["room"]

@fixture(scope="function")
def users(client, room, test_suffix:str):

    user_number:int = 1
    result = []
    for i in range(1, user_number + 1):
        response = client.post(f"/rooms/{room["id"]}/users", json={"username": f"Test User {test_suffix} {i}"})
        if response.status_code != 201:
            raise Exception(f"Failed to create user {i} in room {room["id"]}: {response.json()}")
        result.append(response.json())
    return result

@fixture(scope="function")
def propositions(client, users):
    film_count_per_user:int = 4
    result = []
    for user in users:
        for _ in range(1, film_count_per_user+1):
            response = client.post(f"/users/{user["id"]}/propositions", json={"film_name": f"Film {film_count}"})
            if response.status_code != 201:
                raise Exception(f"Failed to create proposition for user {user["id"]}: {response.json()}")
            result.append(response.json())
            film_count += 1
    return result

