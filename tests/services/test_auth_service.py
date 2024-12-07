import datetime
import pytest
import bcrypt
import jwt
from app.services.auth_service import AuthService
from app.models import User, db

def test_register_user(app):
    AuthService.create_user("testuser", "password123")
    user = User.query.filter_by(username="testuser").first()

    assert user is not None
    assert bcrypt.checkpw("password123".encode("utf-8"), user.password.encode("utf-8"))

def test_register_user_existing_user(app, add_user):
    add_user(1, username="testuser")
    with pytest.raises(ValueError, match="User already exists"):
        AuthService.create_user("testuser", "password123")

def test_login_user(app, add_user):
    hashed_password = bcrypt.hashpw("password123".encode("utf-8"), bcrypt.gensalt())
    add_user(1, username="testuser", password=hashed_password.decode("utf-8"))

    token = AuthService.generate_jwt(1)
    decoded = jwt.decode(token, "qazwsx12", algorithms=["HS256"])
    assert decoded["user_id"] == 1
