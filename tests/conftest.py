import os
import sys
import pathlib
import shutil
import uuid
import pytest
from fastapi.testclient import TestClient


TEST_DB_PATH = pathlib.Path("test_todo.db")



@pytest.fixture(scope="session")
def test_client():
    # Ensure clean test DB
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()

    # Configure test environment before importing the app
    os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH.as_posix()}"
    os.environ["SECRET_KEY"] = os.environ.get("SECRET_KEY", "test-secret-key")

    # Import app after env and alias are ready
    from importlib import import_module

    app_mod = import_module("python_api.main")
    app = app_mod.app

    client = TestClient(app)
    try:
        yield client
    finally:
        # Ensure client resources are released
        try:
            client.close()
        except Exception:
            pass
        # Dispose SQLAlchemy engine to release SQLite file handle on Windows
        try:
            from importlib import import_module
            db_mod = import_module("python_api.database")
            if hasattr(db_mod, "engine"):
                db_mod.engine.dispose()
        except Exception:
            pass
        # Teardown DB file (ignore if locked)
        try:
            TEST_DB_PATH.unlink(missing_ok=True)
        except Exception:
            pass


@pytest.fixture()
def auth_headers(test_client: TestClient):
    # Register a user and return Authorization headers
    email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    password = "password123"

    resp = test_client.post(
        "/auth/register",
        json={"email": email, "password": password, "username": "tester"},
    )
    assert resp.status_code in (200, 201), resp.text

    # OAuth2PasswordRequestForm expects form fields "username" and "password"
    login = test_client.post(
        "/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login.status_code == 200, login.text
    token = login.json()["accessToken"]
    return {"Authorization": f"Bearer {token}"}
