def test_admin_can_access_admin_area(client):
    client.post(
        "/auth/register",
        json={"username": "adminX", "password": "admin_pass", "role": "admin"},
    )
    login = client.post(
        "/auth/login", json={"username": "adminX", "password": "admin_pass"}
    )
    token = login.json()["access_token"]

    response = client.get(
        "/auth/admin-area", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "Welcome admin" in response.json()["msg"]


def test_pharmacist_can_access_pharmacist_area(client):
    client.post(
        "/auth/register",
        json={"username": "pharm1", "password": "pass", "role": "pharmacist"},
    )
    login = client.post("/auth/login", json={"username": "pharm1", "password": "pass"})
    token = login.json()["access_token"]

    response = client.get(
        "/auth/pharmacist-area", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "Welcome pharmacist" in response.json()["msg"]


def test_customer_cannot_access_admin_area(client):
    client.post(
        "/auth/register",
        json={"username": "custX", "password": "cust_pass", "role": "customer"},
    )
    login = client.post(
        "/auth/login", json={"username": "custX", "password": "cust_pass"}
    )
    token = login.json()["access_token"]

    response = client.get(
        "/auth/admin-area", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


def test_admin_cannot_access_pharmacist_area(client):
    client.post(
        "/auth/register",
        json={"username": "admin5", "password": "adminpass", "role": "admin"},
    )
    login = client.post(
        "/auth/login", json={"username": "admin5", "password": "adminpass"}
    )
    token = login.json()["access_token"]

    response = client.get(
        "/auth/pharmacist-area", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


def test_pharmacist_cannot_access_admin_area(client):
    client.post(
        "/auth/register",
        json={"username": "pharmY", "password": "pharm_pass", "role": "pharmacist"},
    )
    login = client.post(
        "/auth/login", json={"username": "pharmY", "password": "pharm_pass"}
    )
    token = login.json()["access_token"]

    response = client.get(
        "/auth/admin-area", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


def test_pharmacist_cannot_access_customer_area(client):
    client.post(
        "/auth/register",
        json={"username": "pharm5", "password": "pharm_pass", "role": "pharmacist"},
    )
    login = client.post(
        "/auth/login", json={"username": "pharm5", "password": "pharm_pass"}
    )
    token = login.json()["access_token"]

    response = client.get(
        "/auth/customer-area", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


def test_admin_can_view_users(client):
    client.post(
        "/auth/register",
        json={"username": "admin1", "password": "adminpass", "role": "admin"},
    )
    response = client.post(
        "/auth/login", json={"username": "admin1", "password": "adminpass"}
    )
    token = response.json()["access_token"]

    response = client.get("/auth/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_non_admin_cannot_list_users(client):
    client.post(
        "/auth/register",
        json={"username": "pharmZ", "password": "pharm_pass", "role": "pharmacist"},
    )
    login = client.post(
        "/auth/login", json={"username": "pharmZ", "password": "pharm_pass"}
    )
    token = login.json()["access_token"]

    response = client.get("/auth/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403


def test_admin_can_change_user_role(client):
    client.post(
        "/auth/register",
        json={"username": "admin", "password": "pass", "role": "admin"},
    )
    admin_token = client.post(
        "/auth/login", json={"username": "admin", "password": "pass"}
    ).json()["access_token"]

    client.post(
        "/auth/register",
        json={"username": "user1", "password": "1234", "role": "customer"},
    )

    response = client.put(
        "/auth/change-role",
        json={"username": "user1", "new_role": "pharmacist"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert "pharmacist" in response.json()["msg"]


def test_non_admin_cannot_change_role(client):
    client.post(
        "/auth/register",
        json={"username": "pharmA", "password": "pharm_pass", "role": "pharmacist"},
    )
    client.post(
        "/auth/register",
        json={"username": "userA", "password": "user_pass", "role": "customer"},
    )
    login = client.post(
        "/auth/login", json={"username": "pharmA", "password": "pharm_pass"}
    )
    token = login.json()["access_token"]

    response = client.put(
        "/auth/change-role",
        json={"username": "userA", "new_role": "admin"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


def test_admin_can_delete_user(client):
    client.post(
        "/auth/register",
        json={"username": "admin3", "password": "pass", "role": "admin"},
    )
    client.post("/auth/register", json={"username": "victim", "password": "pass"})

    login = client.post("/auth/login", json={"username": "admin3", "password": "pass"})
    token = login.json()["access_token"]

    response = client.delete(
        "/auth/delete-user/victim", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "deleted" in response.json()["msg"]


def test_non_admin_cannot_delete_user(client):
    client.post(
        "/auth/register",
        json={"username": "pharmD", "password": "pharm_pass", "role": "pharmacist"},
    )
    client.post(
        "/auth/register",
        json={"username": "victimE", "password": "victim_pass", "role": "customer"},
    )
    login = client.post(
        "/auth/login", json={"username": "pharmD", "password": "pharm_pass"}
    )
    token = login.json()["access_token"]

    response = client.delete(
        "/auth/delete-user/victimE", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


def test_admin_flow(client):
    client.post(
        "/auth/register", json={"username": "boss", "password": "pw", "role": "admin"}
    )
    client.post(
        "/auth/register",
        json={"username": "alice", "password": "alicepw", "role": "customer"},
    )
    r = client.post("/auth/login", json={"username": "boss", "password": "pw"})
    tk = r.json()["access_token"]

    list_resp = client.get("/auth/users", headers={"Authorization": f"Bearer {tk}"})
    assert list_resp.status_code == 200
    users = list_resp.json()
    assert any(u["username"] == "alice" for u in users)

    cr = client.put(
        "/auth/change-role",
        json={"username": "alice", "new_role": "pharmacist"},
        headers={"Authorization": f"Bearer {tk}"},
    )
    assert cr.status_code == 200

    d = client.delete(
        "/auth/delete-user/alice", headers={"Authorization": f"Bearer {tk}"}
    )
    assert d.status_code == 200


def test_non_pharmacist_cannot_access_pharmacist_area(client):
    client.post(
        "/auth/register",
        json={"username": "custB", "password": "cust_pass", "role": "customer"},
    )
    login = client.post(
        "/auth/login", json={"username": "custB", "password": "cust_pass"}
    )
    token = login.json()["access_token"]

    response = client.get(
        "/auth/pharmacist-area", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403


def test_customer_cannot_delete_user(client):
    client.post(
        "/auth/register",
        json={"username": "cust1", "password": "custpass", "role": "customer"},
    )
    response = client.post(
        "/auth/login", json={"username": "cust1", "password": "custpass"}
    )
    token = response.json()["access_token"]

    response = client.delete(
        "/auth/delete-user/someuser", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
