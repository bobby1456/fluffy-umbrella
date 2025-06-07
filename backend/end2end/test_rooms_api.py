from urllib.parse import quote_plus

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_create_room(client):
    response = client.post("/rooms", json={"name": "Test Create Room"})
    print("Response from create room:", response.json())
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["name"] == "Test Create Room"
    assert response.json()["created_at"] is not None

def test_create_room_name_exists(client, room):
    response = client.post("/rooms", json={"name": room["name"]})
    assert response.status_code == 400
    assert response.json()["detail"] is not None

def test_get_room(client, room):
    response = client.get(f"/rooms/{room['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == room["id"]
    assert response.json()["name"] == "Test Room Get Room"

def test_create_room_invalid_data(client):
    response = client.post("/rooms", json={"name": "   "})
    assert response.status_code == 422
    assert response.json()["detail"] is not None

    response = client.post("/rooms", json={"name": "ab"})
    assert response.status_code == 422
    assert response.json()["detail"] is not None


def test_get_room_by_name(client, room):
    room_name = quote_plus(room["name"])

    response = client.get(f"/rooms/find?name={room_name}")
    assert response.status_code == 200
    assert response.json()["id"] == room["id"]
    assert response.json()["name"] == "Test Room Get Room By Name"

def test_get_room_by_name_not_found(client):
    response = client.get("/rooms/find?name=Nonexistent%20Room")
    assert response.status_code == 404
    assert response.json()["detail"] is not None

def test_get_nonexistent_room(client):
    response = client.get("/rooms/999")
    assert response.status_code == 404
    assert response.json()["detail"] is not None