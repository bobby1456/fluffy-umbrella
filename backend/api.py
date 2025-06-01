from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from urllib.parse import unquote
from repositories.database import DatabaseDep
from repositories.model.proposition import Proposition
from repositories.model.user import User
from repositories.model.room import Room


router = APIRouter()

class RoomCreateRequest(BaseModel):
    name: str
    username: str

class RoomResponse(BaseModel):
    room: Room
    users: list[User]

@router.get("/")
def root():
    return {"message": "Welcome to the Movie Room API!"}

@router.post("/rooms", status_code=201)
def create_room(request: RoomCreateRequest, database: DatabaseDep) -> RoomResponse:
    print("Creating room with request:", request)
    name = request.name.strip()
    username = request.username.strip()
    if not name or not username:
        raise HTTPException(status_code=400, detail="Room name or username cannot be empty")
    if len(name) < 3 or len(username) < 3:
        raise HTTPException(status_code=400, detail="Room and user name must be at least 3 characters long")
    
    room = database.rooms.create_room(Room(
        name=name
    ))
    user = database.users.create_user(User(
        username=username,
        room_id=room.id
    ))
    print(f"Room created with id: {room.id} and user: {user.username}")
    return RoomResponse(
        room=room,
        users=[user]
    )

class AddUserToRoomRequest(BaseModel):
    username: str

@router.post("/rooms/{room_id}/users", status_code=201)
def add_user_to_room(room_id: int, request: AddUserToRoomRequest, database: DatabaseDep):
    print(f"Adding user with username: {request.username} to room with id: {room_id}")
    username = request.username.strip()
    if not username:
        raise HTTPException(status_code=400, detail="Username cannot be empty")
    
    room = database.rooms.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    user:User = User(
        username=username,
        room_id=room_id
    )
    user = database.users.create_user(user)
    return user

@router.get("/rooms")
def get_room(name: str, database: DatabaseDep) -> RoomResponse:
    print(f"Getting room with name: {name}")
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

@router.get("/rooms/{room_id}/propositions")
def get_propositions(room_id: int, database: DatabaseDep) -> list[Proposition]:
    propositions = database.propositions.get_propositions_by_room(room_id)
    if not propositions:
        raise HTTPException(status_code=404, detail="No propositions found for this room")
    
    return propositions

class CreatePropositionRequest(BaseModel):
    film_name: str

@router.post("/users/{user_id}/propositions", status_code=201)
def create_proposition(user_id: int, request: CreatePropositionRequest, database: DatabaseDep) -> Proposition:
    film_name = request.film_name.strip()
    if not film_name:
        raise HTTPException(status_code=400, detail="Film name cannot be empty")
    
    user = database.users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    proposition:Proposition = Proposition(
        film_name=film_name,
        user_id=user_id
    )
    proposition = database.propositions.create_proposition(proposition)
    return proposition