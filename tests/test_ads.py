from fastapi.testclient import TestClient


def test_create_ad(client: TestClient, auth_headers):
    response = client.post(
        "/ads/",
        json={
            "title": "Desk IKEA",
            "description": "very good condition",
            "price": 200,
            "category_id": 2
        },
        headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Desk IKEA"
    assert data["description"] == "very good condition"
    assert data["price"] == 200
    assert data["category_id"] == 2
