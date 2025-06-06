from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from repositories.database import DatabaseDep
from repositories.model.user import User, UserCreate, UserPublic

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserPublic, status_code=201)
def create_user(user_create: UserCreate, database: DatabaseDep):
    print(f"Adding user {user_create}")
    username = user_create.username.strip()
    if not username:
        raise HTTPException(status_code=400, detail="Username cannot be empty")
    
    if len(username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters long")
    
    user_create.username = username
    
    room = database.rooms.get_room(user_create.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    user = database.users.create_user(user_create)
    return user

@router.get("/{user_id}", response_model=UserPublic)
def get_user(user_id: int, database: DatabaseDep):
    user = database.users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user