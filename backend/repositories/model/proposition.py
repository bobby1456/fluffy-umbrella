from typing import Annotated
from pydantic import StringConstraints
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

from repositories.model.vote import VotePublic


class PropositionBase(SQLModel):
    title: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    year: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    imdbid: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    type: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    poster: Annotated[str, StringConstraints(min_length=1, max_length=2000, pattern=r"^https?://.+")]

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
