from datetime import datetime
from typing import Annotated
from pydantic import StringConstraints
from sqlmodel import Field, Relationship, SQLModel

from repositories.model.user import UserPublic

class RoomBase(SQLModel):
    name: Annotated[str, StringConstraints(min_length=3, max_length=100, strip_whitespace=True)]

class Room(RoomBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: str | None  = Field(default=datetime.now(), nullable=False)

    users:list["User"] = Relationship(back_populates="room", sa_relationship_kwargs={"lazy": "joined"})

    def __repr__(self):
        return f"Room(id={self.id}, name={self.name}, password={self.password})"


class RoomCreate(RoomBase):
    pass

class RoomPublic(RoomBase):
    id: int
    created_at: str
 
class RoomPublicWithUsers(RoomPublic):
    users: list[UserPublic] = []

    def __repr__(self):
        return f"RoomPublicWithUsers(id={self.id}, name={self.name}, created_at={self.created_at}, users={self.users})"



