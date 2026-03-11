
import pytest
from fastapi.testclient import TestClient
from fastapi import status





# Import the client fixture from conftest.py
@pytest.fixture
def client_fixture(client):
    return client



category = {
        "id": 1,
        "name": "Accessories"
    }



# Test create a new category endpoint
# Success
def test_create_category_success(client: TestClient):

    # post a new category
    response = client.post("/category/new", json=category)
    assert response.status_code == status.HTTP_200_OK


# Failure
def test_create_category_failure(client: TestClient):

    # post a new category
    response = client.post("/category/new", json=category)
    assert response.status_code == status.HTTP_200_OK

    # post another category
    category2 = {
        "id": 2,
        "name": "Accessories"
    }
    response = client.post("/category/new", json=category2)
    assert response.status_code == status.HTTP_400_BAD_REQUEST



# Test get all categories endpoint
# Success
def test_read_all_categories_success(client: TestClient):
    client.post("/category/new", json=category)
    client.post("/category/new", json={"id": 2,"name": "Cosmetics"})

    response = client.get("/category/all")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Accessories"


# Failure
def test_read_all_categories_failure(client: TestClient):
    client.post("/category/new", json=category)
    client.post("/category/new", json={"id": 2, "name": "Cosmetics"})

    response = client.get("/category/alll")
    assert response.status_code == status.HTTP_404_NOT_FOUND




# Test update category endpoint
# Success
def test_update_category_success(client: TestClient):
    client.post("/category/new", json=category)
    name = category["name"]

    update_category = { "name": "Cosmetics"}
    response = client.put(f"/category/update/{name}", json=update_category)
    assert response.status_code == status.HTTP_200_OK



# Failure
def test_update_category_failure(client: TestClient):
    client.post("/category/new", json=category)
    fake_name = "Cosmetics"

    update_category = { "name": "Cosmetics" }
    response = client.put(f"/category/update/{fake_name}", json=update_category)
    assert response.status_code == status.HTTP_404_NOT_FOUND



# Test delete category endpoint
# Success
def test_delete_category_success(client: TestClient):

    client.post("/category/new", json=category)
    name = category["name"]

    response = client.delete(f"/category/delete/{name}")
    assert response.status_code == status.HTTP_200_OK



# Failure
def test_delete_category_failure(client: TestClient):
    client.post("/category/new", json=category)
    fake_name = "Cosmetics"

    response = client.delete(f"/category/delete/{fake_name}")
    assert response.status_code == status.HTTP_404_NOT_FOUND