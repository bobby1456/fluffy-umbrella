import pytest

def test_create_proposition(client, users):
    response = client.post(f"/propositions", json={"film_name": "Inception", "user_id": users[0]["id"]})
    assert response.status_code == 201
    assert response.json()["film_name"] == "Inception"
    assert response.json()["user_id"] == users[0]["id"]
    assert response.json()["id"] is not None
    assert response.json()["created_at"] is not None
    assert "votes" in response.json()
    assert "user" not in response.json()
    

def test_create_proposition_invalid_data(client):
    response = client.post(f"/propositions", json={})
    assert response.status_code == 422
    assert response.json()["detail"] is not None

@pytest.mark.skip(reason="to implement")
def test_get_propositions(client, users):
    film_count_per_user = 4
    for user in users:
        for i in range(1, film_count_per_user + 1):
            create_response = client.post(f"/propositions", json={"film_name": f"Film {i}", "user_id": user["id"]})
            assert create_response.status_code == 201

    get_response = client.get(f"/rooms/{users[0]["room_id"]}/propositions")
    assert get_response.status_code == 200
    propositions = get_response.json()
    assert len(propositions) == film_count_per_user * len(users)
    assert propositions[0]["user_id"] == users[0]["id"]
    assert propositions[0]["film_name"] == "Film 1"
    assert propositions[-1]["user_id"] == users[-1]["id"]
    assert propositions[film_count_per_user]["user_id"] == users[0]["id"]

def test_get_proposition(client, propositions):
    proposition = propositions[0]
    response = client.get(f"/propositions/{proposition["id"]}")
    assert response.status_code == 200
    assert response.json()["id"] == proposition["id"]
    assert response.json()["film_name"] == proposition["film_name"]
    assert response.json()["user_id"] == proposition["user_id"]