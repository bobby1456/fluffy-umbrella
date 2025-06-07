import pytest

@pytest.mark.asyncio
async def test_search_movies(async_client):
    response = await async_client.get("/movies/search?name=Inception&movie_type=movie")
    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, list)
    assert len(json_data) > 0
    assert "Inception" == json_data[0]["title"]
    assert "movie" == json_data[0]["type"]
    assert "year" in json_data[0]
    assert "imdbid" in json_data[0]
    assert "poster" in json_data[0]

