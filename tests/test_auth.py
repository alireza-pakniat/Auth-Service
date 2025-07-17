import time
from app.jwt_utils import create_access_token, verify_token


def test_register_and_login_and_access(client):
    # 1. Register
    resp = client.post(
        "/auth/register",
        json={"username": "alice", "password": "secret", "role": "customer"},
    )
    assert resp.status_code == 200
    assert "registered" in resp.json()["msg"]

    # 2. Register duplicate → 400
    resp2 = client.post(
        "/auth/register",
        json={"username": "alice", "password": "x", "role": "customer"},
    )
    assert resp2.status_code == 400

    # 3. Login success
    login = client.post("/auth/login", json={"username": "alice", "password": "secret"})
    assert login.status_code == 200
    token = login.json()["access_token"]

    # 4. Access protected route without token → 401
    no_token = client.get("/auth/admin-only")
    assert no_token.status_code == 401

    # 5. Access admin-only with customer token → 403
    res403 = client.get(
        "/auth/admin-only", headers={"Authorization": f"Bearer {token}"}
    )
    assert res403.status_code == 403


def test_admin_flow(client):
    # Register admin user
    client.post(
        "/auth/register", json={"username": "boss", "password": "pw", "role": "admin"}
    )
    # Login as admin
    r = client.post("/auth/login", json={"username": "boss", "password": "pw"})
    tk = r.json()["access_token"]

    # List users (now alice and boss exist)
    list_resp = client.get("/auth/users", headers={"Authorization": f"Bearer {tk}"})
    assert list_resp.status_code == 200
    users = list_resp.json()
    assert any(u["username"] == "alice" for u in users)

    # Change alice → pharmacist
    cr = client.put(
        "/auth/change-role",
        json={"username": "alice", "new_role": "pharmacist"},
        headers={"Authorization": f"Bearer {tk}"},
    )
    assert cr.status_code == 200

    # Delete alice
    d = client.delete(
        "/auth/delete-user/alice", headers={"Authorization": f"Bearer {tk}"}
    )
    assert d.status_code == 200
