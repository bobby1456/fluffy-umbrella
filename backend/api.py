from fastapi import FastAPI, HTTPException
from repositories.db import Database
from pydantic import BaseModel
from urllib.parse import unquote

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie Night API!"}

class RoomCreateRequest(BaseModel):
    name: str
    username: str

@app.post("/rooms", status_code=201)
def create_room(request: RoomCreateRequest):
    print("Creating room with request:", request)
    name = request.name.strip()
    username = request.username.strip()
    if not name or not username:
        raise HTTPException(status_code=400, detail="Room name or username cannot be empty")
    if len(name) < 3 or len(username) < 3:
        raise HTTPException(status_code=400, detail="Room and user name must be at least 3 characters long")
    
    room_id = Database().rooms.create_room(name)
    user_id = Database().users.create_user(username, room_id)
    user = Database().users.get_user(user_id)
    return {
        "room": {
            "id": room_id,
            "name": name,
        },
        "users": [user]
    }

class AddUserToRoomRequest(BaseModel):
    username: str

@app.post("/rooms/{room_id}/users", status_code=201)
def add_user_to_room(room_id: int, request: AddUserToRoomRequest):
    print(f"Adding user with username: {request.username} to room with id: {room_id}")
    username = request.username.strip()
    if not username:
        raise HTTPException(status_code=400, detail="Username cannot be empty")
    
    room = Database().rooms.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    user_id = Database().users.create_user(username, room_id)
    user = Database().users.get_user(user_id)
    return user

@app.get("/rooms")
def get_room(name: str):
    print(f"Getting room with name: {name}")
    decoded_room_name = unquote(name.strip())
    room = Database().rooms.get_room_by_name(decoded_room_name)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    users = Database().rooms.get_users_in_room(room["id"])
    return {
        "room": {
            "id": room["id"],
            "name": room["name"],
        },
        "users": users
    }

@app.get("rooms/{room_id}")
def get_room_by_id(room_id: int):
    room = Database().rooms.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    users = Database().rooms.get_users_in_room(room_id)
    return {
        "room": {
            "id": room["id"],
            "name": room["name"],
        },
        "users": users
    }

@app.get("/rooms/{room_id}/propositions")
def get_propositions(room_id: int):
    propositions = Database().propositions.get_propositions_by_room(room_id)
    if not propositions:
        raise HTTPException(status_code=404, detail="No propositions found for this room")
    
    return propositions

class CreatePropositionRequest(BaseModel):
    film_name: str

@app.post("/users/{user_id}/propositions", status_code=201)
def create_proposition(user_id: int, request: CreatePropositionRequest):
    film_name = request.film_name.strip()
    if not film_name:
        raise HTTPException(status_code=400, detail="Film name cannot be empty")
    
    user = Database().users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    proposition_id = Database().propositions.create_proposition(user_id, film_name)
    return {"proposition_id": proposition_id, "film_name": film_name}