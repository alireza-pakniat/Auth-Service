# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app import models

# Create a separate test database (in-memory or file-based)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # For persistent test DB
# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # For in-memory (optional)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ✅ Override the dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Apply override before tests run
app.dependency_overrides[get_db] = override_get_db


# ✅ Fixture to initialize and clean DB
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ✅ Fixture to provide a test client
@pytest.fixture()
def client():
    return TestClient(app)
