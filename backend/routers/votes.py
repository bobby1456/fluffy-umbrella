from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from repositories.database import DatabaseDep
from repositories.model.vote import VoteCreate, VotePublic

router = APIRouter(prefix="/votes", tags=["votes"])

@router.post("", response_model=VotePublic, status_code=201)
def vote_on_proposition(vote_create: VoteCreate, database: DatabaseDep):
    user = database.users.get_user(vote_create.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    proposition = database.propositions.get_proposition(vote_create.proposition_id)
    if not proposition:
        raise HTTPException(status_code=404, detail="Proposition not found")
    
    if vote_create.value not in ["up", "down"]:
        raise HTTPException(status_code=400, detail="Vote must be 'up' or 'down'")
    
    vote = database.votes.create_vote(vote_create)
    return vote

@router.get("/{vote_id}", response_model=VotePublic)
def get_vote(vote_id: int, database: DatabaseDep):
    vote = database.votes.get_vote(vote_id)
    if not vote:
        raise HTTPException(status_code=404, detail="Vote not found")
    
    return vote