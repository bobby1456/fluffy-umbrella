from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from repositories.database import DatabaseDep
from repositories.model.proposition import Proposition, PropositionCreate, PropositionPublic
from repositories.model.vote import Vote


router = APIRouter()

class CreatePropositionRequest(BaseModel):
    film_name: str

@router.post("/users/{user_id}/propositions", status_code=201)
def create_proposition(user_id: int, request: CreatePropositionRequest, database: DatabaseDep) -> PropositionPublic:
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

@router.get("/propositions/{proposition_id}", response_model=PropositionPublic)
def get_proposition(proposition_id: int, database: DatabaseDep) -> PropositionPublic:
    proposition = database.propositions.get_proposition(proposition_id)
    if not proposition:
        raise HTTPException(status_code=404, detail="Proposition not found")
    
    return proposition