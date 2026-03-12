import pytest
from main import app
from schemas.user import UserDisplay
from auth.oauth2 import get_current_user
from fastapi import status, HTTPException
from fastapi.testclient import TestClient


# Import the client fixture from conftest.py
@pytest.fixture
def client_fixture(client):
    return client

user = {
    "username": "Ivan",
    "email": "ivan@gmail.com",
    "password": "ivan1",
    "confirm_password": "ivan1"
}

user2 = {
    "username": "cat",
    "email": "cat@gmail.com",
    "password": "cat1",
    "confirm_password": "cat1"
}


login_data = {
    "email": "ivan@gmail.com",
    "password": "ivan1"
}

login_data2 = {
    "email": "cat@gmail.com",
    "password": "cat1"
}

ad = {
  "title": "Ring",
  "description": "A golden ring, 21k , 20gm",
  "price": 2000,
  "category_id": 1
}

category = {
    "id": 1,
    "name": "Accessories"
}


# Test rate an ad
# Success
def test_rating_ad_success(client: TestClient):
    # create users
    client.post("/user", json=user)
    client.post("/user", json=user2)

    # seller login
    login_response = client.post("/user/login", json=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # override current user as seller
    app.dependency_overrides[get_current_user] = lambda: UserDisplay(id=1, username="Ivan", email="ivan@gmail.com")
    try:
        # create category and ad
        client.post("/category/new", json=category)
        create_ad_response = client.post("/ads/", json=ad, headers=headers)
        assert create_ad_response.status_code == 201

        # update ad status to SOLD
        status_update = {"status": "SOLD", "buyer_id": 2}
        ad_id = 1
        response = client.patch(f"/ads/{ad_id}/status?id={ad_id}", json=status_update, headers=headers)
        assert response.status_code == status.HTTP_200_OK

        # buyer login
        login_buyer_response = client.post("/user/login", json=login_data2)
        buyer_token = login_buyer_response.json()["access_token"]
        buyer_headers = {"Authorization": f"Bearer {buyer_token}"}

        # override current user as buyer
        app.dependency_overrides[get_current_user] = lambda: UserDisplay(id=2, username="cat", email="cat@gmail.com")

        # buyer rates the ad
        rating_payload = {"score": 5}
        rating_response = client.post(f"/ratings/ads/{ad_id}", json=rating_payload, headers=buyer_headers)
        print(rating_response.json())
        assert rating_response.status_code == status.HTTP_201_CREATED
        assert rating_response.json()["score"] == 5
        assert rating_response.json()["rater_id"] == 2
        assert rating_response.json()["ad_id"] == ad_id
    finally:
        app.dependency_overrides.pop(get_current_user, None)

# Failure
def test_rating_not_existing_ad_failure(client: TestClient):
    # create users
    client.post("/user", json=user)
    client.post("/user", json=user2)

    # seller login
    login_response = client.post("/user/login", json=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # override current user as seller
    app.dependency_overrides[get_current_user] = lambda: UserDisplay(id=1, username="Ivan", email="ivan@gmail.com")
    try:
        # create category and ad
        client.post("/category/new", json=category)
        create_ad_response = client.post("/ads/", json=ad, headers=headers)
        assert create_ad_response.status_code == 201

        # update ad status to SOLD
        status_update = {"status": "SOLD", "buyer_id": 2}
        ad_id = 1
        response = client.patch(f"/ads/{ad_id}/status?id={ad_id}", json=status_update, headers=headers)
        assert response.status_code == status.HTTP_200_OK

        # buyer login
        login_buyer_response = client.post("/user/login", json=login_data2)
        buyer_token = login_buyer_response.json()["access_token"]
        buyer_headers = {"Authorization": f"Bearer {buyer_token}"}

        # override current user as buyer
        app.dependency_overrides[get_current_user] = lambda: UserDisplay(id=2, username="cat", email="cat@gmail.com")

        # buyer rates the ad
        rating_payload = {"score": 5}
        rating_response = client.post(f"/ratings/ads/{10}", json=rating_payload, headers=buyer_headers)
        print(rating_response.json())
        assert rating_response.status_code == status.HTTP_404_NOT_FOUND
    finally:
        app.dependency_overrides.pop(get_current_user, None)

def test_rating_ad_not_SOLD_failure(client: TestClient):
    # create users
    client.post("/user", json=user)
    client.post("/user", json=user2)

    # seller login
    login_response = client.post("/user/login", json=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # override current user as seller
    app.dependency_overrides[get_current_user] = lambda: UserDisplay(id=1, username="Ivan", email="ivan@gmail.com")
    try:
        # create category and ad
        client.post("/category/new", json=category)
        create_ad_response = client.post("/ads/", json=ad, headers=headers)
        assert create_ad_response.status_code == 201

        # update ad status to SOLD
        status_update = {"status": "RESERVED", "buyer_id": 2}
        ad_id = 1
        response = client.patch(f"/ads/{ad_id}/status?id={ad_id}", json=status_update, headers=headers)
        assert response.status_code == status.HTTP_200_OK

        # buyer login
        login_buyer_response = client.post("/user/login", json=login_data2)
        buyer_token = login_buyer_response.json()["access_token"]
        buyer_headers = {"Authorization": f"Bearer {buyer_token}"}

        # override current user as buyer
        app.dependency_overrides[get_current_user] = lambda: UserDisplay(id=2, username="cat", email="cat@gmail.com")

        # buyer rates the ad
        rating_payload = {"score": 5}
        rating_response = client.post(f"/ratings/ads/{ad_id}", json=rating_payload, headers=buyer_headers)
        print(rating_response.json())
        assert rating_response.status_code == status.HTTP_400_BAD_REQUEST
    finally:
        app.dependency_overrides.pop(get_current_user, None)
