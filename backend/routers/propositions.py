from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from repositories.database import DatabaseDep
from repositories.model.proposition import Proposition, PropositionCreate
from repositories.model.vote import Vote


router = APIRouter()

class CreatePropositionRequest(BaseModel):
    film_name: str

@router.post("/users/{user_id}/propositions", status_code=201)
def create_proposition(user_id: int, request: CreatePropositionRequest, database: DatabaseDep) -> Proposition:
    film_name = request.film_name.strip()
    if not film_name:
        raise HTTPException(status_code=400, detail="Film name cannot be empty")
    
    user = database.users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    proposition = PropositionCreate(
        film_name=film_name,
        user_id=user_id
    )
    return database.propositions.create_proposition(proposition)