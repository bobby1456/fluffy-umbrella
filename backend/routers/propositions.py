from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from repositories.database import DatabaseDep
from repositories.model.proposition import Proposition, PropositionCreate, PropositionPublic
from repositories.model.vote import Vote


router = APIRouter(prefix="/propositions", tags=["propositions"])

@router.post("", status_code=201)
def create_proposition(proposition_create: PropositionCreate, database: DatabaseDep) -> PropositionPublic:
    film_name = proposition_create.film_name.strip()
    if not film_name:
        raise HTTPException(status_code=400, detail="Film name cannot be empty")
    proposition_create.film_name = film_name

    user = database.users.get_user(proposition_create.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return database.propositions.create_proposition(proposition_create)

@router.get("/{proposition_id}", response_model=PropositionPublic)
def get_proposition(proposition_id: int, database: DatabaseDep) -> PropositionPublic:
    proposition = database.propositions.get_proposition(proposition_id)
    if not proposition:
        raise HTTPException(status_code=404, detail="Proposition not found")
    
    return proposition