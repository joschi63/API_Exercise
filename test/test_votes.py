def test_vote_on_post(authorized_client, test_posts, test_user2):
    response = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert response.status_code == 201

def test_vote_on_own_post(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert response.status_code == 403

def test_vote_twice_on_post(authorized_client, test_posts, test_user2):
    authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    response = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert response.status_code == 409

def test_remove_vote_on_post(authorized_client, test_posts):
    authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    response = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert response.status_code == 201

def test_remove_nonexistent_vote(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert response.status_code == 404

def test_vote_on_non_exist_post(authorized_client, test_posts):
    response = authorized_client.post("/vote/", json={"post_id": "8000000", "dir": 1})
    assert response.status_code == 404
