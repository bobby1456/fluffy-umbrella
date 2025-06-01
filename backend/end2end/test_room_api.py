def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_create_room(client):
    response = client.post("/rooms", json={"name": "Test Create Room", "username": "Test User Create Room"})
    print("Response from create room:", response.json())
    assert response.status_code == 201
    assert "room" in response.json()
    assert "users" in response.json()
    assert "id" in response.json()["room"]
    assert response.json()["room"]["name"] == "Test Create Room"
    assert response.json()["users"][0]["id"] is not None
    assert response.json()["users"][0]["username"] == "Test User Create Room"
    assert response.json()["users"][0]["room_id"] == response.json()["room"]["id"]
    assert response.json()["users"][0]["created_at"] is not None

def test_create_room_invalid_data(client):
    response = client.post("/rooms", json={"name": "  ", "username": "  "})
    assert response.status_code == 400
    assert response.json()["detail"] is not None

    response = client.post("/rooms", json={"name": "ab", "username": "ab"})
    assert response.status_code == 400
    assert response.json()["detail"] is not None

def test_get_room_by_name(client):
    create_response = client.post("/rooms", json={"name": "Test Room Get Room", "username": "Test User Get Room"})
    assert create_response.status_code == 201
    room_id = create_response.json()["room"]["id"]

    response = client.get(f"/rooms?name=Test%20Room%20Get%20Room")
    assert response.status_code == 200
    assert response.json()["room"]["id"] == room_id
    assert response.json()["room"]["name"] == "Test Room Get Room"
    assert len(response.json()["users"]) > 0 
    assert response.json()["users"][0]["username"] == "Test User Get Room"

def test_get_nonexistent_room(client):
    response = client.get("/rooms/Nonexistent+Room")
    assert response.status_code == 404
    assert response.json()["detail"] is not None