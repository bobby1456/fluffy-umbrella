from fastapi import APIRouter, HTTPException
import apis.movies_api as movies_api

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/search", response_model=list[movies_api.Movie])
async def search_movies(name: str, movie_type:str):
    if not name:
        raise HTTPException(status_code=400, detail="Movie name cannot be empty")
    
    if movie_type not in ["movie", "series"]:
        raise HTTPException(status_code=400, detail="Invalid movie type. Must be 'movie' or 'series'")
    
    movies = await movies_api.search_movies(name.strip(), movie_type)
    
    return movies