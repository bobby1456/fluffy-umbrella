def test_create_user(client, room):
    response = client.post(f"/users", json={"username": "Test User Create", "room_id": room["id"]})
    assert response.status_code == 201
    assert response.json()["username"] == "Test User Create"
    assert response.json()["room_id"] == room["id"]
    assert response.json()["id"] is not None
    assert response.json()["created_at"] is not None
    assert "room" not in response.json()

def test_create_multiple_users_in_room(client, room):
    user_count = 5
    for i in range(user_count):
        create_response = client.post(f"/users", json={"username": f"User {i + 1}", "room_id": room["id"]})
        assert create_response.status_code == 201
        assert create_response.json()["username"] == f"User {i + 1}"
        assert create_response.json()["room_id"] == room["id"]

    get_response = client.get(f"/rooms/{room["id"]}")
    print("response path", get_response.url)
    print("Response from get room:", get_response.json())
    assert get_response.status_code == 200
    users = get_response.json()["users"]
    assert len(users) == user_count
    for i in range(user_count):
        assert users[i]["username"] == f"User {i + 1}"
        assert users[i]["room_id"] == room["id"]

def test_create_user_invalid_data(client, room):
    response = client.post(f"/users", json={"username": "  ", "room_id": room["id"]})
    assert response.status_code == 422
    assert response.json()["detail"] is not None

    response = client.post(f"/users", json={"username": "a", "room_id": room["id"]})
    assert response.status_code == 422
    assert response.json()["detail"] is not None

    response = client.post(f"/users", json={})
    assert response.status_code == 422
    assert response.json()["detail"] is not None

def test_add_user_to_nonexistent_room(client):
    response = client.post("/users", json={"username": "Test User Nonexistent Room", "room_id": 999})
    assert response.status_code == 404
    assert response.json()["detail"] is not None

def test_get_user(client, users):
    user = users[0]
    response = client.get(f"/users/{user['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == user["id"]
    assert response.json()["username"] == user["username"]
    assert response.json()["room_id"] == user["room_id"]