
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
        "username": "Heba",
        "email": "heba@gmail.com",
        "password": "hs123",
        "confirm_password": "hs123"
    }

login_data = {
        "email": "heba@gmail.com",
        "password": "hs123"
    }


# Test create user endpoint
# Success
def test_create_user_success(client: TestClient):

    # post a new user
    response = client.post("/user/", json=user)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["username"] == "Heba"
    assert data["email"] == "heba@gmail.com"



# Failure
def test_create_user_email_exists(client: TestClient):

    # post a new user
    response1 = client.post("/user/", json=user)
    assert response1.status_code == status.HTTP_201_CREATED

    user2 = {
        "username": "Hapi",
        "email": "heba@gmail.com",
        "password": "hs123",
        "confirm_password": "hs123"
    }
    response2 = client.post("/user/", json=user2)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST



def test_create_user_password_mismatch(client: TestClient):

    # post a new user
    user = {
        "username": "Heba",
        "email": "heba@gmail.com",
        "password": "hs123",
        "confirm_password": "123hs"
    }

    response = client.post("/user/", json=user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY



# Test user login endpoint
# Success
def test_login_success(client: TestClient):

    # post a new user
    response = client.post("/user/", json=user)
    assert response.status_code == status.HTTP_201_CREATED

    response = client.post("/user/login", json=login_data)
    assert response.status_code == status.HTTP_200_OK



# Failure
def test_login_failure(client: TestClient):

    # post a new user
    response = client.post("/user/", json=login_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY



# Test user logout endpoint
# Success
def test_logout(client: TestClient):

    # post a new user
    response = client.post("/user/logout")
    assert response.status_code == status.HTTP_200_OK




# Test read user by id endpoint
# Success
def test_get_user_success(client: TestClient):

    # post a new user
    create_response = client.post("/user/", json=user)
    assert create_response.status_code == status.HTTP_201_CREATED
    user_id = create_response.json()["id"]

    # override get_current_user
    def override_get_current_user():
        return UserDisplay(id=1, username="Heba", email="heba@gmail.com")

    app.dependency_overrides[get_current_user] = override_get_current_user

    # login to get the token
    login_response = client.post("/user/login", json=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]
    headers = {"Authorization": "Bearer " + token}

    # call the protected endpoint
    get_response = client.get(f"/user/{user_id}", headers=headers)
    assert get_response.status_code == status.HTTP_200_OK

    # clean override
    app.dependency_overrides.pop(override_get_current_user, None)



# Failure
def test_get_user_failure_not_found(client: TestClient):

    fake_user_id = 99999

    # override get_current_user
    def override_get_current_user():
        return UserDisplay(id=1, username="Heba", email="heba@gmail.com")

    app.dependency_overrides[get_current_user] = override_get_current_user

    headers = {"Authorization": "Bearer faketoken"}
    response = client.get(f"/user/{fake_user_id}", headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    app.dependency_overrides.pop(override_get_current_user, None)



def test_get_user_failure_unauthorized(client: TestClient):
    user_id = 1
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.get(f"/user/{user_id}", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND



# Test user update endpoint
# Success
def test_update_user_success(client: TestClient):

    # post a new user
    create_response = client.post("/user/", json=user)
    assert create_response.status_code == status.HTTP_201_CREATED
    user_id = create_response.json()["id"]

    # login to get the token
    login_response = client.post("/user/login", json=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]
    headers = {"Authorization": "Bearer " + token}

    # update user data
    updated_user = {
        "username": "Hapi",
        "email": "hapi@gmail.com",
        "password": "123hs",
        "confirm_password": "123hs"
    }
    update_response = client.put(f"/user/{user_id}/update", json=updated_user, headers=headers)
    assert update_response.status_code == status.HTTP_200_OK



# Failure
def test_update_user_failure_user_not_found(client: TestClient):

    # post a new user
    create_response = client.post("/user/", json=user)
    assert create_response.status_code == status.HTTP_201_CREATED

    # login to get a token
    login_response = client.post("/user/login", json=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": "Bearer " + token}


    fake_user_id = 99999

    # update user data
    updated_user = {
        "username": "Hapi",
        "email": "hapi@gmail.com",
        "password": "123hs",
        "confirm_password": "123hs"
    }

    response = client.put(f"/user/{fake_user_id}/update", json=updated_user, headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND



def test_update_user_failure_invalid_token(client: TestClient):

    # post a new user
    create_response = client.post("/user/", json=user)
    assert create_response.status_code == status.HTTP_201_CREATED
    user_id = create_response.json()["id"]

    # override get_current_user
    def override_get_current_user():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    app.dependency_overrides[get_current_user] = override_get_current_user

    # login to get a token
    client.post("/user/login", json=login_data)
    headers = {"Authorization": "Bearer faketoken"}

    # update user data
    updated_user = {
        "username": "Hapi",
        "email": "hapi@gmail.com",
        "password": "123hs",
        "confirm_password": "123hs"
    }
    response = client.put(f"/user/{user_id}/update", json=updated_user, headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    app.dependency_overrides.pop(override_get_current_user, None)



# Test delete user endpoint
# Success
def test_delete_user_success(client: TestClient):

    # post a new user
    create_response = client.post("/user/", json=user)
    assert create_response.status_code == status.HTTP_201_CREATED
    user_id = create_response.json()["id"]

    # login to get token
    login_response = client.post("/user/login", json=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]
    headers = {"Authorization": "Bearer " + token}

    # override get_current_user
    def override_get_current_user():
        return {"username": "Heba", "email": "heba@gmail.com", "password": "hs123"}
    app.dependency_overrides[get_current_user] = override_get_current_user

    # delete user
    delete_response = client.delete(f"/user/delete/{user_id}", headers=headers)
    assert delete_response.status_code == status.HTTP_200_OK

    app.dependency_overrides.pop(override_get_current_user, None)


# Failure
def test_delete_user_failure_user_not_found(client: TestClient):

    # post a new user
    create_response = client.post("/user/", json=user)
    assert create_response.status_code == status.HTTP_201_CREATED
    fake_user_id = 99999

    # login to get a token
    login_response = client.post("/user/login", json=login_data)
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]
    headers = {"Authorization": "Bearer " + token}

    # override get_current_user
    def override_get_current_user():
        return  UserDisplay(id=fake_user_id, username="Heba", email="heba@gmail.com")
    app.dependency_overrides[get_current_user] = override_get_current_user

    # delete a user
    delete_response = client.delete(f"/user/delete/{fake_user_id}", headers=headers)
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND

    app.dependency_overrides.pop(override_get_current_user, None)



def test_delete_user_failure_invalid_token(client: TestClient):

    # post a new user
    create_response = client.post("/user/", json=user)
    assert create_response.status_code == status.HTTP_201_CREATED
    user_id = create_response.json()["id"]

    # override get_current_user
    def override_get_current_user():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    app.dependency_overrides[get_current_user] = override_get_current_user

    # delete user
    headers = {"Authorization": "Bearer faketoken"}
    delete_response = client.delete(f"/user/delete/{user_id}", headers=headers)
    assert delete_response.status_code == status.HTTP_401_UNAUTHORIZED

    app.dependency_overrides.pop(override_get_current_user, None)