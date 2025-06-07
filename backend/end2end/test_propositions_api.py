test_movie = {
    "title": "Game of Thrones",
    "year": "2011–2019",
    "imdbid": "tt0944947",
    "type": "series",
    "poster": "https://m.media-amazon.com/images/M/MV5BMTNhMDJmNmYtNDQ5OS00ODdlLWE0ZDAtZTgyYTIwNDY3OTU3XkEyXkFqcGc@._V1_SX300.jpg"
} 

def test_create_proposition(client, users):
    response = client.post(f"/propositions", json={"user_id": users[0]["id"], **test_movie})
    assert response.status_code == 201
    assert response.json()["user_id"] == users[0]["id"]
    assert response.json()["id"] is not None
    assert response.json()["created_at"] is not None

    assert response.json()["imdbid"] == test_movie["imdbid"]
    assert response.json()["year"] == test_movie["year"]
    assert response.json()["type"] == test_movie["type"]
    assert response.json()["poster"] == test_movie["poster"]
    assert response.json()["title"] == test_movie["title"]

    assert "votes" in response.json()
    assert "user" not in response.json()
    
def test_create_proposition_invalid_data(client):
    response = client.post(f"/propositions", json={})
    assert response.status_code == 422
    assert response.json()["detail"] is not None

def test_create_proposition_without_movie(client, users):
    response = client.post(f"/propositions", json={"user_id": users[0]["id"]})
    assert response.status_code == 422
    assert response.json()["detail"] is not None

def test_get_proposition(client, propositions):
    proposition = propositions[0]
    response = client.get(f"/propositions/{proposition["id"]}")
    assert response.status_code == 200
    assert response.json()["id"] == proposition["id"]
    assert response.json()["created_at"] == proposition["created_at"]
    assert response.json()["user_id"] == proposition["user_id"]
    assert response.json()["imdbid"] == proposition["imdbid"]
    assert response.json()["year"] == proposition["year"]
    assert response.json()["type"] == proposition["type"]
    assert response.json()["poster"] == proposition["poster"]
    assert response.json()["title"] == proposition["title"]