def test_create_user(client, room):
    response = client.post(f"/rooms/{room["id"]}/users", json={"username": "Test User Create"})
    assert response.status_code == 201
    assert response.json()["username"] == "Test User Create"
    assert response.json()["room_id"] == room["id"]

def test_create_multiple_users_in_room(client, room):
    user_count = 5
    for i in range(user_count):
        create_response = client.post(f"/rooms/{room['id']}/users", json={"username": f"User {i + 1}"})
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
    response = client.post(f"/rooms/{room["id"]}/users", json={"username": "  "})
    assert response.status_code == 400
    assert response.json()["detail"] is not None

    response = client.post(f"/rooms/{room["id"]}/users", json={"username": "ab"})
    assert response.status_code == 400
    assert response.json()["detail"] is not None

    response = client.post(f"/rooms/{room["id"]}/users", json={})
    assert response.status_code == 422
    assert response.json()["detail"] is not None

def test_add_user_to_nonexistent_room(client):
    response = client.post("/rooms/999/users", json={"username": "Test User Nonexistent Room"})
    assert response.status_code == 404
    assert response.json()["detail"] is not None

