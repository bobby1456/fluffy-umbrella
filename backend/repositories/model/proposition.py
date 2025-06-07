from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

from repositories.model.vote import VotePublic


class PropositionBase(SQLModel):
    title: str = Field(nullable=True)
    year: str = Field(nullable=True)
    imdbid: str = Field(nullable=True)
    type: str = Field(nullable=True) 
    poster: str = Field(nullable=True)

    user_id: int = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")

class Proposition(PropositionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: str | None = Field(default=datetime.now(), nullable=False)
    
    user:"User" = Relationship(back_populates="propositions")
    votes: list["Vote"] = Relationship(back_populates="proposition")
        
class PropositionCreate(PropositionBase):
    pass
    

class PropositionPublic(PropositionBase):
    id: int
    created_at: str
    votes: list[VotePublic] = []
