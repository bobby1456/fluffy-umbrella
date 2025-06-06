from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from repositories.database import DatabaseDep
from repositories.model.user import User, UserCreate, UserPublic

router = APIRouter()

class AddUserToRoomRequest(BaseModel):
    username: str

    
@router.post("/rooms/{room_id}/users", response_model=UserPublic, status_code=201)
def add_user_to_room(room_id: int, request: AddUserToRoomRequest, database: DatabaseDep):
    print(f"Adding user with username: {request.username} to room with id: {room_id}")
    username = request.username.strip()
    if not username:
        raise HTTPException(status_code=400, detail="Username cannot be empty")
    
    if len(username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters long")
    
    room = database.rooms.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    user:UserCreate = UserCreate(
        username=username,
        room_id=room_id
    )
    user = database.users.create_user(user)
    return user

@router.get("/users/{user_id}", response_model=UserPublic)
def get_user(user_id: int, database: DatabaseDep):
    user = database.users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user