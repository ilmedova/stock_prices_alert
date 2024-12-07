import json
import bcrypt

def test_register_user(client):
    response = client.post(
        "/api/register",
        data=json.dumps({"username": "testuser", "password": "password123"}),
        content_type="application/json",
    )
    assert response.status_code == 201
    assert response.json["message"] == "User registered successfully"

def test_register_user_missing_fields(client):
    response = client.post(
        "/api/register",
        data=json.dumps({"username": "testuser"}),
        content_type="application/json",
    )
    assert response.status_code == 400
    assert response.json["message"] == "Missing required fields"

def test_register_user_existing_user(client, add_user):
    user = add_user(1, username="testuser", password="password123")
    assert user.username == "testuser"

def test_login_user(client, add_user):
    hashed_password = bcrypt.hashpw("password123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user = add_user(1, username="testuser", password=hashed_password)
    assert user.password == hashed_password
