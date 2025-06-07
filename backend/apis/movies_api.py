
from pydantic import BaseModel
from httpx import AsyncClient
from fastapi import HTTPException

from repositories.model.movie import MovieCreate

class OmdbMovie(BaseModel):
    Title: str
    Year: int
    imdbID: str
    Type: str
    Poster: str

    def to_create(self) -> MovieCreate:
        return MovieCreate(
            title=self.Title,
            year=self.Year,
            imdbid=self.imdbID,
            type=self.Type,
            poster=self.Poster
        )


class OmbdMoviesSearchResult(BaseModel):
    Search: list[OmdbMovie]
    totalResults: str
    Response: str

client: AsyncClient = AsyncClient(base_url="http://www.omdbapi.com", params={"apikey": "3391f096"})

async def search_movies(name:str, movie_type:str) -> list[MovieCreate]:
    response = await client.get("", params={"s": name, "type": movie_type})
    if response.status_code != 200:
        raise HTTPException(502, f"Error fetching data from OMDB API: {response.text}")
    
    result = OmbdMoviesSearchResult.model_validate(response.json())
    if result.Response == "False":
        raise HTTPException(502, f"OMDB API error: {result.Search}")
    
    return [movie.to_create() for movie in result.Search]

