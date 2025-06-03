from urllib.parse import unquote
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from repositories.database import DatabaseDep
from repositories.model.room import Room
from repositories.model.user import User

router = APIRouter()

class RoomCreateRequest(BaseModel):
    name: str

class RoomResponse(BaseModel):
    room: Room
    users: list[User]


@router.post("/rooms", status_code=201)
def create_room(request: RoomCreateRequest, database: DatabaseDep) -> RoomResponse:
    print("Creating room with request:", request)
    name = request.name.strip()

    if not name:
        raise HTTPException(status_code=400, detail="Room name or username cannot be empty")
    if len(name) < 3:
        raise HTTPException(status_code=400, detail="Room and user name must be at least 3 characters long")
    
    room = database.rooms.create_room(Room(
        name=name
    ))
    print(f"Room created: {room}")
    return RoomResponse(
        room=room,
        users=[]
    )

@router.get("/rooms/find")
def get_room(name: str, database: DatabaseDep) -> RoomResponse:
    print(f"Getting room with name: {name}")
    if not name:
        raise HTTPException(status_code=400, detail="Room name cannot be empty")
    decoded_room_name = unquote(name.strip())
    room = database.rooms.get_room_by_name(decoded_room_name)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    users = database.users.get_users_in_room(room.id)
    return RoomResponse(
        room=room,
        users=users
    )

@router.get("rooms/{room_id}")
def get_room_by_id(room_id: int, database: DatabaseDep) -> RoomResponse:
    room = database.rooms.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    users = database.users.get_users_in_room(room_id)
    return RoomResponse(
        room=room,
        users=users
    )
