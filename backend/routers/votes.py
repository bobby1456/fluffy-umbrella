from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from repositories.database import DatabaseDep
from repositories.model.vote import VoteCreate, VotePublic

router = APIRouter()

class VoteRequest(BaseModel):
    user_id: int
    vote:str # "up" or "down"

@router.post("/{proposition_id}/vote", response_model=VotePublic, status_code=201)
def vote_on_proposition(proposition_id: int, request: VoteRequest, database: DatabaseDep):
    user = database.users.get_user(request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    proposition = database.propositions.get_proposition(proposition_id)
    if not proposition:
        raise HTTPException(status_code=404, detail="Proposition not found")
    
    if request.vote not in ["up", "down"]:
        raise HTTPException(status_code=400, detail="Vote must be 'up' or 'down'")
    
    vote = database.votes.create_vote(VoteCreate(
        proposition_id=proposition_id,
        user_id=request.user_id,
        vote=request.vote)
    )
    
    return vote
