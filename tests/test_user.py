
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base
from main import app
from database import db_user

# Test database in memory
TEST_DB_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False}).connect()
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create database prior to any test
@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    # sleep(5)
    Base.metadata.create_all(bind=test_engine)
    print(f"\nSetting up")
    yield
    print(f"\nTearing down")
    Base.metadata.drop_all(bind=test_engine)

client = TestClient(app)

def test_create_user_endpoint():
    response = client.post("/users",
                           json={"name": "Rens",
                                 "email": "rens@example.com"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Rens"
    assert data["email"] == "rens@example.com"
    assert data["id"] == 1




if __name__ == "__main__":
    exit_code = pytest.main(["tests/", "-v"])
    print(f"Tests completed with exit code {exit_code}")