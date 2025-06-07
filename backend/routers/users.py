from fastapi import APIRouter, HTTPException

from repositories.database import DatabaseDep
from repositories.model.user import UserCreate, UserPublic

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserPublic, status_code=201)
def create_user(user_create: UserCreate, database: DatabaseDep):
    username = user_create.username.strip()
    
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