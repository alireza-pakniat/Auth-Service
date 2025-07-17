from app.jwt_utils import create_access_token, verify_token
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def test_register_and_login_and_access(client):
    resp = client.post(
        "/auth/register",
        json={"username": "alice", "password": "secret", "role": "customer"},
    )
    assert resp.status_code == 200
    assert "registered" in resp.json()["msg"]

    resp2 = client.post(
        "/auth/register",
        json={"username": "alice", "password": "x", "role": "customer"},
    )
    assert resp2.status_code == 400

    login = client.post("/auth/login", json={"username": "alice", "password": "secret"})
    assert login.status_code == 200
    token = login.json()["access_token"]

    no_token = client.get("/auth/admin-area")
    assert no_token.status_code == 401

    res403 = client.get(
        "/auth/admin-area", headers={"Authorization": f"Bearer {token}"}
    )
    assert res403.status_code == 403


def test_token_creation_and_verification():
    data = {"sub": "testuser", "role": "admin"}
    token = create_access_token(data)
    decoded = verify_token(token)
    assert decoded["sub"] == "testuser"
    assert decoded["role"] == "admin"


def test_password_hashing():
    pw = "secret123"
    hashed = pwd_context.hash(pw)
    assert pwd_context.verify(pw, hashed)
