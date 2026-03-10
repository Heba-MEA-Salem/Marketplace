import pytest
from main import app
from fastapi import status
from fastapi.testclient import TestClient





# Import the client fixture from conftest.py
@pytest.fixture
def client_fixture(client):
    return client


user = {
    "username": "Heba",
    "email": "heb@gmail.com",
    "password": "hs123",
    "confirm_password": "hs123"
}



# Test get_token endpoint
# Success
def test_get_token_success(client: TestClient):

    # post a new user
    create_response = client.post("/user/", json=user)
    assert create_response.status_code == status.HTTP_201_CREATED

    # request token
    response = client.post("/token", data={"username": "Heba", "password": "hs123"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["username"] == "Heba"
    print("Created access token", data["access_token"])




# Failure
def test_get_token_wrong_password(client: TestClient):

    client.post("/user/", json=user)

    response = client.post("/token", data={"username": "Heba", "password": "123hs"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Incorrect Password"



def test_get_token_user_not_found(client: TestClient):

    client.post("/user/", json=user)

    response = client.post("/token", data={"username": "FakeUser", "password": "hs123"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Invalid Credentials"