from fastapi.testclient import TestClient
from starlette import status

ad_data = {
    "title": "Desk IKEA",
    "description": "very good condition",
    "price": 200,
    "category_id": 2
}

updated_ad_data = {
    "title": "Desk IKEA Updated",
    "description": "still in very good condition",
    "price": 250,
    "category_id": 2
}


# Test create ad
def test_create_ad_success(client: TestClient, auth_headers):
    response = client.post(
        "/ads",
        json=ad_data,
        headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Desk IKEA"
    assert data["description"] == "very good condition"
    assert data["price"] == 200
    assert data["category_id"] == 2


# Failure
def test_create_ad_invalid_price(client: TestClient, auth_headers):
    invalid_ad_data = {
        "title": "Desk IKEA",
        "description": "very good condition",
        "price": -10,
        "category_id": 2
    }

    response = client.post(
        "/ads",
        json=invalid_ad_data,
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# Test get ad by id endpoint

def test_get_ad_success(client: TestClient, auth_headers):
    create_response = client.post(
        "/ads",
        json=ad_data,
        headers=auth_headers
    )
    assert create_response.status_code == status.HTTP_201_CREATED

    created_ad = create_response.json()
    ad_id = created_ad["id"]

    response = client.get(f"/ads/{ad_id}", headers=auth_headers)

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()
    ad = response_data["data"]

    assert ad["id"] == ad_id
    assert ad["title"] == "Desk IKEA"
    assert ad["description"] == "very good condition"
    assert ad["price"] == 200
    assert ad["category_id"] == 2


# Failure
def test_get_ad_not_found(client: TestClient, auth_headers):
    response = client.get("/ads/999", headers=auth_headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert "detail" in data


# Test update ad
# Success
def test_update_ad_success(client: TestClient, auth_headers):
    create_response = client.post(
        "/ads",
        json=ad_data,
        headers=auth_headers
    )
    assert create_response.status_code == status.HTTP_201_CREATED

    created_ad = create_response.json()
    ad_id = created_ad["id"]

    response = client.patch(
        f"/ads/{ad_id}",
        json=updated_ad_data,
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == ad_id
    assert data["title"] == "Desk IKEA Updated"
    assert data["description"] == "still in very good condition"
    assert data["price"] == 250
    assert data["category_id"] == 2


# Test delete_ad
# Success

def test_delete_ad_success(client: TestClient, auth_headers):
    create_response = client.post(
        "/ads",
        json=ad_data,
        headers=auth_headers
    )
    assert create_response.status_code == status.HTTP_201_CREATED

    created_ad = create_response.json()
    ad_id = created_ad["id"]

    delete_response = client.delete(f"/ads/{ad_id}", headers=auth_headers)

    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    get_response = client.get(f"/ads/{ad_id}", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


# Filter ads by category
def test_filter_ads_by_category(client: TestClient, auth_headers):
    client.post("/ads", json=ad_data, headers=auth_headers)

    response = client.get("/ads/filtered?category_id=2", headers=auth_headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert len(data) >= 1
    assert all(ad["category_id"] == 2 for ad in data)


# Search ads by query
def test_filter_ads_by_query(client: TestClient, auth_headers):
    client.post("/ads", json=ad_data, headers=auth_headers)

    response = client.get("/ads/filtered?q=Desk", headers=auth_headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert len(data) >= 1
    assert any("Desk" in ad["title"] for ad in data)


# partial update ads
def test_partial_update_ad_success(client: TestClient, auth_headers):
    create_response = client.post(
        "/ads",
        json=ad_data,
        headers=auth_headers
    )
    assert create_response.status_code == status.HTTP_201_CREATED

    ad_id = create_response.json()["id"]

    partial_update_data = {
        "price": 180
    }

    response = client.patch(
        f"/ads/{ad_id}",
        json=partial_update_data,
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["price"] == 180
    assert data["title"] == "Desk IKEA"
    assert data["description"] == "very good condition"
    assert data["category_id"] == 2
