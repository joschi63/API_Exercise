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

