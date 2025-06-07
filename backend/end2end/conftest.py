from typing import AsyncGenerator, Generator
from httpx import ASGITransport, AsyncClient
import pytest_asyncio
from starlette.testclient import TestClient
from fastapi import FastAPI
from pytest import fixture, FixtureRequest
from .movies_data import movies
from repositories import database
from api import router

@fixture(scope="session")
def app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app

@fixture(scope="session", autouse=True)
def client(app)-> Generator[TestClient]:
    db_config = database.DatabaseEngineConfig(db_file_name="test_database.db")
    database.init_engine(db_config)

    yield TestClient(app)
    database.destroy()

@pytest_asyncio.fixture(scope="module")
async def async_client(app) -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

@fixture(scope="function")
def test_suffix(request:FixtureRequest):
    return request.function.__name__.replace("test_", "").replace("_", " ").title()

@fixture(scope="function")
def room(client, test_suffix:str):
    response = client.post("/rooms", json={"name": f"Test Room {test_suffix}", "username": f"Test User {test_suffix}"})
    if response.status_code != 201:
        raise Exception(f"Failed to create room: {response.json()}")
    return response.json()

@fixture(scope="function")
def users(client, room, test_suffix:str):

    user_number:int = 1
    result = []
    for i in range(1, user_number + 1):
        response = client.post(f"/users", json={"username": f"Test User {test_suffix} {i}", "room_id": room["id"]})
        if response.status_code != 201:
            raise Exception(f"Failed to create user {i} in room {room["id"]}: {response.json()}")
        result.append(response.json())
    return result


@fixture(scope="function")
def room_with_user(room, users):
    return room

# manage case where users makes a proposition that already exists
@fixture(scope="function")
def propositions(client, users):
    film_count_per_user:int = 4
    result = []
    film_count:int = 0
    for user in users:
        for _ in range(1, film_count_per_user+1):
            response = client.post(f"/propositions", json={"user_id": user["id"], **movies[film_count]})
            if response.status_code != 201:
                raise Exception(f"Failed to create proposition for user {user["id"]}: {response.json()}")
            result.append(response.json())
            film_count += 1
    return result

