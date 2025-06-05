from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

from repositories.model.vote import VotePublic


class PropositionBase(SQLModel):
    film_name: str = Field(index=True, nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False, ondelete="CASCADE")

class Proposition(PropositionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: str | None = Field(default=datetime.now(), nullable=False)
    
    user:"User" = Relationship(back_populates="propositions")
    votes: list["Vote"] = Relationship(back_populates="proposition")

    def __repr__(self):
        return f"Proposition(id={self.id}, film_name={self.film_name}, user_id={self.user_id})"
    
class PropositionCreate(PropositionBase):
    pass

class PropositionPublic(PropositionBase):
    id: int
    created_at: str
    votes: list[VotePublic] = []

    def __repr__(self):
        return f"PropositionPublic(id={self.id}, film_name={self.film_name}, user_id={self.user_id}, created_at={self.created_at})"