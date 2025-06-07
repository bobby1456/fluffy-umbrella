from urllib.parse import unquote
from fastapi import APIRouter, HTTPException
from repositories.database import DatabaseDep
from repositories.model.room import RoomCreate, RoomPublicWithUsers

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.post("", response_model=RoomPublicWithUsers, status_code=201)
def create_room(room_create: RoomCreate, database: DatabaseDep):
    print("Creating room with request:", room_create)
    name = room_create.name.strip()

    if not name:
        raise HTTPException(status_code=400, detail="Room name or username cannot be empty")
    if len(name) < 3:
        raise HTTPException(status_code=400, detail="Room and user name must be at least 3 characters long")
    
    room_create.name = name
    
    room = database.rooms.create_room(room_create)
    print(f"Room created: {room}")
    return room

@router.get("/find", response_model=RoomPublicWithUsers)
def get_room(name: str,  database: DatabaseDep):
    print(f"Getting room with name: {name}")
    if not name:
        raise HTTPException(status_code=400, detail="Room name cannot be empty")
    decoded_room_name = unquote(name.strip())
    room = database.rooms.get_room_by_name(decoded_room_name)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    

    return room

@router.get("/{room_id}", response_model=RoomPublicWithUsers)
def get_room_by_id(room_id: int, database: DatabaseDep):
    room = database.rooms.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    print("room users",room.users)
    
    return room
