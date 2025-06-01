from sqlmodel import Field, SQLModel
from datetime import datetime

class Room(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False)
    created_at: str = Field(default=datetime.now(), nullable=False)

    def __repr__(self):
        return f"Room(id={self.id}, name={self.name}, password={self.password})"