from sqlmodel import Field, SQLModel
from datetime import datetime

class Proposition(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    film_name: str = Field(index=True, nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    created_at: str = Field(default=datetime.now(), nullable=False)

    def __repr__(self):
        return f"Proposition(id={self.id}, film_name={self.film_name}, user_id={self.user_id})"