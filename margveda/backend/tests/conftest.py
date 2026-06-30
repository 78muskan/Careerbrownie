"""
Shared pytest fixtures for Career Brownie backend tests.
Uses an in-memory SQLite database so tests are isolated and fast.
"""
import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./careerbrownie-test.db")
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production")
os.environ.setdefault("ENVIRONMENT", "test")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.api.dependencies import get_db
from app.main import create_app

TEST_DB_URL = "sqlite:///./careerbrownie-test.db"

engine_test = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture()
def db():
    connection = engine_test.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="session")
def client():
    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture()
def registered_student(client):
    payload = {
        "full_name": "Test Student",
        "email": "student@test.careerbrownie.com",
        "password": "testpass123",
        "role": "student",
    }
    r = client.post("/api/v1/auth/register", json=payload)
    if r.status_code == 409:
        r = client.post("/api/v1/auth/login", json={"email": payload["email"], "password": payload["password"]})
    return r.json()


@pytest.fixture()
def registered_counsellor(client):
    payload = {
        "full_name": "Test Counsellor",
        "email": "counsellor@test.careerbrownie.com",
        "password": "testpass123",
        "role": "counsellor",
    }
    r = client.post("/api/v1/auth/register", json=payload)
    if r.status_code == 409:
        r = client.post("/api/v1/auth/login", json={"email": payload["email"], "password": payload["password"]})
    return r.json()


@pytest.fixture()
def student_headers(registered_student):
    return {"Authorization": f"Bearer {registered_student['access_token']}"}


@pytest.fixture()
def counsellor_headers(registered_counsellor):
    return {"Authorization": f"Bearer {registered_counsellor['access_token']}"}
