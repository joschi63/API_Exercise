import pytest
import jwt

import app.token_managing as tm 
from app.config import settings 

email = "user3@gmail.com"
password = "password123"

def test_create_user(client):
    response = client.post(
        "/users/",
        json= {
            "email": email,
            "password": password
        }
    )
    assert response.json().get("email") == email
    assert response.status_code == 201


def test_login_user(client, test_user):
    response = client.post(
        "/login", 
        data= {
            "username": test_user['email'],
            "password": test_user['password']
        }
    )
    login_res = tm.Token(**response.json())
    payload = jwt.decode(
            login_res.access_token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code, detail", [
    ("wrongemail@gmail.com", "password123", 403, "Invalid Credentials"),
    ("user3@gmail.com", "wrongpassword", 403, "Invalid Credentials"),
    (None, "password123", 422, "No username or password provided"),
    ("user3@gmail.com", None, 422, "No username or password provided"), 
    (None, None, 422, "No username or password provided"),
    ])
def test_incorrect_login(client, test_user, email, password, status_code, detail):
    response = client.post(
        "/login", 
        data= {
            "username": email,
            "password": password
        }
    )
    assert response.status_code == status_code
    assert response.json().get("detail") == detail
