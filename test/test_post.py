import pytest
from typing import List
from app.models import post_models


#@pytest.mark.parametrize("title, content", [("first title", "first content")])


# def test_createposts(authorized_client, test_posts):
#     response = authorized_client.post(
#         "/posts/",
#         data={
#             "title": title,
#             "content": content
#         }
#     )
#     print(response.json())
#     assert response.status_code == 201

def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    # posts = [post_models.PostOut(**post) for post in response.json()]
    # print(posts)

    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200

def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = post_models.PostOut(**response.json())

    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert response.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")

    assert response.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/999999")
    assert response.status_code == 404

@pytest.mark.parametrize("title, content, published", [
    ("new title 1", "new content 1", True),
    ("new title 2", "new content 2", False),
    ("new title 3", "new content 3", True),
    ])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    response = authorized_client.post("/posts/", json= {
        "title": title,
        "content": content,
        "published": published
    })
    created_post = post_models.PostRead(**response.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']
    assert response.status_code == 201

def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    response = authorized_client.post("/posts/", json= {
        "title": "title1",
        "content": "content1",
        #"published": True
    })
    print(response.json())
    created_post = post_models.PostRead(**response.json())
    assert created_post.title == "title1"
    assert created_post.content == "content1"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']
    assert response.status_code == 201

def test_unauthorized_user_create_post(client, test_posts, test_user):
    response = client.post("/posts/", json= {
        "title": "title1",
        "content": "content1",
        "published": True
    })
    assert response.status_code == 401


def test_delte_post_success(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_delete_post_not_exist(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/99999")
    assert response.status_code == 404

def test_delete_other_user_post(authorized_client, test_posts, test_user):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert response.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": False,
        "id": test_posts[0].id
    }

    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = post_models.PostRead(**response.json())
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert updated_post.published == data['published']
    assert response.status_code == 200

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": False,
        "id": test_posts[3].id
    }

    response = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert response.status_code == 403

def test_unauthorized_user_update_post(client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": False,
        "id": test_posts[0].id
    }

    response = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert response.status_code == 401

def test_update_post_not_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": False,
        "id": 99999
    }

    response = authorized_client.put(f"/posts/99999", json=data)
    assert response.status_code == 404