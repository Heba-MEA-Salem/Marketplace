from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db.database import get_db
from db.models import Base, DbCategory
from main import app
import pytest


# Test database in memory
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
).connect()
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)

# Override the get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


def seed_test_categories():
    db = TestingSessionLocal()
    try:
        if db.query(DbCategory).count() == 0:
            db.add_all([
                DbCategory(id=1, name="Electronics"),
                DbCategory(id=2, name="Furniture"),
                DbCategory(id=3, name="Clothing"),
                DbCategory(id=4, name="Jewelry"),
                DbCategory(id=5, name="Appliances"),
            ])
            db.commit()
    finally:
        db.close()

# Setup and teardown for every test
@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=test_engine)
    seed_test_categories()
    print("\n Setting up")
    yield
    Base.metadata.drop_all(bind=test_engine)
    print("\n Tearing down")


# Test client ficture
@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_headers(client: TestClient):
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
        "confirm_password": "testpassword"
    }

    create_response = client.post("/user/", json=user_data)
    assert create_response.status_code == 201

    login_response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


