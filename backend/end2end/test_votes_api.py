def test_vote_on_proposition(client, propositions, users):
    proposition = propositions[0]
    user = users[-1]

    response = client.post(f"/votes", json={"user_id": user["id"], "proposition_id": proposition["id"] , "value": "up"})
    assert response.status_code == 201
    assert response.json()["proposition_id"] == proposition["id"]
    assert response.json()["user_id"] == user["id"]
    assert response.json()["value"] == "up"
    assert response.json()["id"] is not None
    assert response.json()["created_at"] is not None
    assert "proposition" not in response.json()
    assert "user" not in response.json()

    get_vote_response = client.get(f"/votes/{response.json()['id']}")
    assert get_vote_response.status_code == 200
    vote = get_vote_response.json()

    get_response = client.get(f"/propositions/{proposition['id']}")
    assert get_response.status_code == 200
    assert "votes" in get_response.json()
    votes = get_response.json()["votes"]
    assert len(votes) == 1
    assert votes[0]["user_id"] == user["id"]
    assert votes[0]["id"] == vote["id"]

def test_vote_on_nonexistent_proposition(client, users):
    user = users[0]
    response = client.post("/propositions/999/votes", json={"user_id": user["id"], "value": "up"})
    assert response.status_code == 404
    assert response.json()["detail"] is not None

def test_vote_on_proposition_by_nonexistent_user(client, propositions):
    proposition = propositions[0]
    response = client.post(f"/votes", json={"user_id": 999, "proposition_id":proposition["id"], "value": "up"})
    assert response.status_code == 404
    assert response.json()["detail"] is not None

def test_vote_on_proposition_invalid_data(client, propositions, users):
    proposition = propositions[0]
    user = users[0]

    response = client.post(f"/votes", json={})
    assert response.status_code == 422
    assert response.json()["detail"] is not None

    response = client.post(f"/votes", json={"user_id": user["id"], "proposition_id":proposition["id"], "value": "invalid"})
    assert response.status_code == 400
    assert response.json()["detail"] is not None