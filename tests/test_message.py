import pytest
from main import app
from schemas.user import UserDisplay
from auth.oauth2 import get_current_user
from fastapi.testclient import TestClient
from fastapi import status, HTTPException


# Import the client fixture from conftest.py
@pytest.fixture
def client_fixture(client):
    return client


user = {
    "username": "Heba",
    "email": "heba@gmail.com",
    "password": "hs123",
    "confirm_password": "hs123"
}

user2 = {
    "username": "Hapi",
    "email": "hapi@gmail.com",
    "password": "hs123",
    "confirm_password": "hs123"
}


login_data = {
    "email": "heba@gmail.com",
    "password": "hs123"
}

ad = {
  "title": "Ring",
  "description": "A golden ring, 21k , 20gm",
  "price": 2000,
  "category_id": 1
}

ad2 = {
    "title": "Ring",
    "description": "A sliver ring, 925k , 10gm",
    "price": 200,
    "category_id": 1
}

category = {
    "id": 1,
    "name": "Accessories"
}

message = {
  "ad_id": 1,
  "buyer_id": 1,
  "seller_id": 2,
  "message_body": "Is this product still available"
}



# Test  create a message endpoint
# Success
def test_create_message(client: TestClient):

    # post users
    client.post("/user", json=user)
    client.post("/user", json=user2)

    # login to get a token
    login_response = client.post("/user/login", json=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}


    # override get_current_user
    def override_get_current_user():
        return UserDisplay(id=1, username="Heba", email="heba@gmail.com")

    app.dependency_overrides[get_current_user] = override_get_current_user

    # post an ad and a category
    client.post("/category/new", json=category)
    client.post("/ads/", json=ad)


    # call the protected endpoint
    response = client.post("/message/", json=message, headers=headers)
    assert response.status_code == status.HTTP_200_OK

    app.dependency_overrides.pop(override_get_current_user, None)




# Failure
def test_create_message_failure_existing_message(client: TestClient):
    # post users
    client.post("/user", json=user)
    client.post("/user", json=user2)

    # login to get a token
    login_response = client.post("/user/login", json=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # override get_current_user
    def override_get_current_user():
        return UserDisplay(id=1, username="Heba", email="heba@gmail.com")

    app.dependency_overrides[get_current_user] = override_get_current_user

    # post an ad and a category
    client.post("/category/new", json=category)
    client.post("/ads/", json=ad)


    # call the protected endpoint
    message2 = {
        "ad_id": 1,
        "buyer_id": 1,
        "seller_id": 2,
        "message_body": "Is this product still available"
    }
    client.post("/message/", json=message, headers=headers)
    response = client.post("/message/", json=message2, headers=headers)
    assert response.status_code == status.HTTP_409_CONFLICT


    app.dependency_overrides.pop(override_get_current_user, None)




def test_create_message_failure(client: TestClient):
    client.post("/user", json=user)

    # login to get a token
    login_response = client.post("/user/login", json=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}


    # override get_current_user
    def override_get_current_user():
        return UserDisplay(id=1, username="Heba", email="heba@gmail.com")

    app.dependency_overrides[get_current_user] = override_get_current_user

    # call the protected endpoint
    response = client.post("/message/", json=message, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    app.dependency_overrides.pop(override_get_current_user, None)




# Test  get a message endpoint
# Success
def test_read_all_message_success(client: TestClient):
    # post users
    client.post("/user", json=user)
    client.post("/user", json=user2)

    # login to get a token
    login_response = client.post("/user/login", json=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # override get_current_user
    def override_get_current_user():
        return UserDisplay(id=1, username="Heba", email="heba@gmail.com")

    app.dependency_overrides[get_current_user] = override_get_current_user

    # post ads and a category

    client.post("/category/new", json=category)
    client.post("/ads/", json=ad)
    client.post("/ads/", json=ad2)

    # post messages
    message2 = {
        "ad_id": 1,
        "buyer_id": 2,
        "seller_id": 1,
        "message_body": "I want two pieces"
    }
    client.post("/message/", json=message, headers=headers)
    client.post("/message/", json=message2, headers=headers)

    response = client.get("/message/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    app.dependency_overrides.pop(override_get_current_user, None)




# Failure
def test_read_all_message_failure(client: TestClient):

    # post users
    client.post("/user", json=user)
    client.post("/user", json=user2)

    # login to get a token
    login_response = client.post("/user/login", json=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # override get_current_user
    def override_get_current_user():
        return UserDisplay(id=1, username="Heba", email="heba@gmail.com")

    app.dependency_overrides[get_current_user] = override_get_current_user


    # post ads and a category
    client.post("/category/new", json=category)
    client.post("/ads/", json=ad)
    client.post("/ads/", json=ad2)


    response = client.get("/message/", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    app.dependency_overrides.pop(override_get_current_user, None)
