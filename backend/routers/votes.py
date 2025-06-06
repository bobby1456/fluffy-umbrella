from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from repositories.database import DatabaseDep
from repositories.model.vote import VoteCreate, VotePublic

router = APIRouter()

class VoteRequest(BaseModel):
    user_id: int
    value:str # "up" or "down"

@router.post("/propositions/{proposition_id}/votes", response_model=VotePublic, status_code=201)
def vote_on_proposition(proposition_id: int, request: VoteRequest, database: DatabaseDep):
    user = database.users.get_user(request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    proposition = database.propositions.get_proposition(proposition_id)
    if not proposition:
        raise HTTPException(status_code=404, detail="Proposition not found")
    
    if request.value not in ["up", "down"]:
        raise HTTPException(status_code=400, detail="Vote must be 'up' or 'down'")
    
    vote = database.votes.create_vote(VoteCreate(
        proposition_id=proposition_id,
        user_id=request.user_id,
        value=request.value)
    )
    
    return vote

@router.get("/votes/{vote_id}", response_model=VotePublic)
def get_vote(vote_id: int, database: DatabaseDep):
    vote = database.votes.get_vote(vote_id)
    if not vote:
        raise HTTPException(status_code=404, detail="Vote not found")
    
    return vote