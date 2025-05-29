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

    name = request.name.strip()
    username = request.username.strip()
    if not name or not username:
        raise HTTPException(status_code=400, detail="Room name or username cannot be empty")
    if len(name) < 3 or len(username) < 3:
        raise HTTPException(status_code=400, detail="Room and user name must be at least 3 characters long")
    
    room_id = Database().rooms.create_room(name)
    user_id = Database().users.create_user(username, room_id)
    return {
        "room": {
            "id": room_id,
            "name": name,
        },
        "user": {
            "username": username,
            "user_id": user_id
        }
    }

@app.get("/rooms/{room_name}")
def get_room(room_name: str):
    decoded_room_name = unquote(room_name.strip())
    room = Database().rooms.get_room_by_name(decoded_room_name)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    print(f"Retrieved room: {room}")
    
    users = Database().rooms.get_users_in_room(room[0])
    return {
        "room": {
            "id": room[0],
            "name": room[1],
        },
        "users": users
    }