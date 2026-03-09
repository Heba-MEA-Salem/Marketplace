from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db.database import get_db
from db.models import Base
from main import app
import pytest


# Test database in memory
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False}).connect()
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Override the get_db dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


# Setup and teardown for every test
@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=test_engine)
    print(f"\n Setting up")
    yield
    Base.metadata.drop_all(bind=test_engine)
    print(f"\n Tearing down")


# Test client ficture
@pytest.fixture
def client():
    return TestClient(app)