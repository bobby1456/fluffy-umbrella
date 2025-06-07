from urllib.parse import unquote
from fastapi import APIRouter, HTTPException
from repositories.database import DatabaseDep
from repositories.model.room import RoomCreate, RoomPublicWithUsers

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.post("", response_model=RoomPublicWithUsers, status_code=201)
def create_room(room_create: RoomCreate, database: DatabaseDep):
    name = room_create.name.strip()

    if database.rooms.get_room_by_name(name):
        raise HTTPException(status_code=400, detail="Room with this name already exists")

    room_create.name = name
    
    room = database.rooms.create_room(room_create)
    return room

@router.get("/find", response_model=RoomPublicWithUsers)
def get_room(name: str,  database: DatabaseDep):
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
    
    return room
