from fastapi import APIRouter
from routers import rooms, users, propositions, votes, movies


router = APIRouter()
router.include_router(rooms.router, tags=["rooms"])
router.include_router(users.router, tags=["users"])
router.include_router(propositions.router, tags=["propositions"])
router.include_router(votes.router, tags=["votes"])
router.include_router(movies.router, tags=["movies"])

@router.get("/")
def root():
    return {"message": "Welcome to the Movie Room API!"}


