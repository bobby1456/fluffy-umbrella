from sqlmodel import Field, SQLModel
from datetime import datetime

class Vote(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    proposition_id: int = Field(foreign_key="proposition.id", nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    created_at: str = Field(default=datetime.now(), nullable=False)


    def __repr__(self):
        return f"Vote(id={self.id}, proposition_id={self.proposition_id}, user_id={self.user_id})"