from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime


class VoteBase(SQLModel):
    proposition_id: int = Field(foreign_key="proposition.id", nullable=False, ondelete="CASCADE")
    user_id: int = Field(foreign_key="user.id", nullable=False)
    value:str = Field(index=True, nullable=False) 

class Vote(VoteBase, table=True):
    id: int |None = Field(default=None, primary_key=True)

    proposition: "Proposition" = Relationship(back_populates="votes")
    user: "User" = Relationship(back_populates="votes")

    created_at: str = Field(default=datetime.now(), nullable=False)

    def __repr__(self):
        return f"Vote(id={self.id}, proposition_id={self.proposition_id}, user_id={self.user_id})"
    
class VoteCreate(VoteBase):
    pass

class VotePublic(VoteBase):
    id: int
    created_at: str

    def __repr__(self):
        return f"VotePublic(id={self.id}, proposition_id={self.proposition_id}, user_id={self.user_id}, created_at={self.created_at})"