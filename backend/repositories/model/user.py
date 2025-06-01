
from sqlmodel import Field, SQLModel
from datetime import datetime

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False)
    room_id: int = Field(foreign_key="room.id", nullable=False)
    created_at: str = Field(default=datetime.now(), nullable=False)
