def test_create_user(client, room):
    response = client.post(f"/rooms/{room["id"]}/users", json={"username": "Test User Create"})
    assert response.status_code == 201
    assert response.json()["username"] == "Test User Create"
    assert response.json()["room_id"] == room["id"]

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