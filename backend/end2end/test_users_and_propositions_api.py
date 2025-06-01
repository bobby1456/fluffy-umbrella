def room_and_user_setup(client, test_suffix:str):
    response = client.post("/rooms", json={"name": f"Test Room {test_suffix}", "username": f"Test User {test_suffix}"})
    assert response.status_code == 201
    return response.json()["room"]["id"], response.json()["users"][0]["id"]

def add_users_to_room_setup(client, room_id, test_suffix:str, user_number:int = 1):
    user_ids = []
    for i in range(1, user_number + 1):
        response = client.post(f"/rooms/{room_id}/users", json={"username": f"Test User {test_suffix} {i}"})
        assert response.status_code == 201
        assert response.json()["username"] == f"Test User {test_suffix} {i}"
        assert response.json()["room_id"] == room_id
        assert response.json()["id"] is not None
        assert response.json()["created_at"] is not None
        user_ids.append(response.json()["id"])
        user_ids.append(response.json()["id"])
    return user_ids

def test_create_proposition(client):
    _, user_id = room_and_user_setup(client, "Create Proposition")
    response = client.post(f"/users/{user_id}/propositions", json={"film_name": "Inception"})
    assert response.status_code == 201
    assert response.json()["film_name"] == "Inception"
    assert response.json()["user_id"] == user_id

def test_create_proposition_invalid_data(client):
    _, user_id = room_and_user_setup(client, "Invalid Data")
    response = client.post(f"/users/{user_id}/propositions", json={"film_name": "  "})
    assert response.status_code == 400
    assert response.json()["detail"] is not None

    response = client.post(f"/users/{user_id}/propositions", json={})
    assert response.status_code == 422
    assert response.json()["detail"] is not None

def test_create_room_add_users_and_get_propositions(client):
    room_id, user_id = room_and_user_setup(client, "Get Propositions")
    users_ids = add_users_to_room_setup(client, room_id, "Get Propositions", 2)

    film_count_per_user = 4
    film_count = 1
    for user_id in users_ids:
        for _ in range(1, film_count_per_user+1):
            response = client.post(f"/users/{user_id}/propositions", json={"film_name": f"Film {film_count}"})
            assert response.status_code == 201 
            film_count += 1

    response = client.get(f"/rooms/{room_id}/propositions")
    assert response.status_code == 200
    propositions = response.json()
    assert len(propositions) == film_count_per_user * len(users_ids)
    assert all("film_name" in proposition for proposition in propositions)
    assert all("user_id" in proposition for proposition in propositions)

    assert response.json()[film_count_per_user]["film_name"] == "Film 5"
    assert response.json()[film_count_per_user]["user_id"] == users_ids[1]
    assert response.json()[film_count_per_user - 1]["user_id"] == users_ids[0]
