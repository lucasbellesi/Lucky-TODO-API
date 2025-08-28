def test_register_and_login_flow(test_client):
    email = "alice@example.com"
    password = "password123"

    r = test_client.post("/auth/register", json={"email": email, "password": password, "username": "alice"})
    assert r.status_code in (200, 201), r.text
    data = r.json()
    assert data["email"] == email
    assert "id" in data

    # Duplicate register should fail
    r2 = test_client.post("/auth/register", json={"email": email, "password": password, "username": "alice2"})
    assert r2.status_code == 400

    # Login (form-encoded, username field carries the email)
    login = test_client.post(
        "/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login.status_code == 200, login.text
    tokens = login.json()
    assert "accessToken" in tokens
    assert "refreshToken" in tokens
    assert tokens["expiresIn"] > 0

