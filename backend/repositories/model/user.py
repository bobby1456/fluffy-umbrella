
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

from repositories.model.proposition import Proposition, PropositionPublic
from repositories.model.vote import Vote

class UserBase(SQLModel):
    username: str = Field(index=True, nullable=False)
    room_id: int = Field(foreign_key="room.id", nullable=False, ondelete="CASCADE")

class UserCreate(UserBase):
    pass

class UserPublic(UserBase):
    id: int
    created_at: str
    propositions: list[PropositionPublic] = []


class User(UserBase, table=True):
    id: int |None = Field(default=None, primary_key=True)
    created_at: str | None = Field(default=datetime.now(), nullable=False) 
    
    room: "Room" = Relationship(back_populates="users")

    propositions: list[Proposition] = Relationship(back_populates="user")
    votes: list[Vote] = Relationship(back_populates="user")

