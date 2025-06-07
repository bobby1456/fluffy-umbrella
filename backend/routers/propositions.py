from fastapi import APIRouter, HTTPException
from repositories.database import DatabaseDep
from repositories.model.proposition import PropositionCreate, PropositionPublic


router = APIRouter(prefix="/propositions", tags=["propositions"])

@router.post("", status_code=201)
def create_proposition(proposition_create: PropositionCreate, database: DatabaseDep) -> PropositionPublic:
    user = database.users.get_user(proposition_create.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = database.propositions.create_proposition(proposition_create)
    print(f"Created proposition: {result}")
    return PropositionPublic.model_validate(result)

@router.get("/{proposition_id}", response_model=PropositionPublic)
def get_proposition(proposition_id: int, database: DatabaseDep) -> PropositionPublic:
    proposition = database.propositions.get_proposition(proposition_id)
    if not proposition:
        raise HTTPException(status_code=404, detail="Proposition not found")
    
    return proposition