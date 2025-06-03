from urllib.parse import quote_plus

from repositories.model.room import Room

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_create_room(client):
    response = client.post("/rooms", json={"name": "Test Create Room"})
    print("Response from create room:", response.json())
    assert response.status_code == 201
    assert "id" in response.json()["room"]
    assert response.json()["room"]["name"] == "Test Create Room"
 
def test_create_room_invalid_data(client):
    response = client.post("/rooms", json={"name": "  ", "username": "  "})
    assert response.status_code == 400
    assert response.json()["detail"] is not None

    response = client.post("/rooms", json={"name": "ab", "username": "ab"})
    assert response.status_code == 400
    assert response.json()["detail"] is not None

def test_get_room_by_name(client, room):
    room_name = quote_plus(room["name"])

    response = client.get(f"/rooms/find?name={room_name}")
    assert response.status_code == 200
    assert response.json()["room"]["id"] == room["id"]
    assert response.json()["room"]["name"] == "Test Room Get Room By Name"
    assert len(response.json()["users"]) == 0 

def test_get_nonexistent_room(client):
    response = client.get("/rooms/Nonexistent+Room")
    assert response.status_code == 404
    assert response.json()["detail"] is not None