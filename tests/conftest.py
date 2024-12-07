import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from app import create_app, db
from app.models import User

@pytest.fixture(scope="module")
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="module")
def client(app):
    return app.test_client()

@pytest.fixture(scope="function")
def init_database(app):
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()
        yield db.session
        db.session.remove()

@pytest.fixture
def add_user(init_database):
    def _add_user(id, username="testuser", password="testpassword"):
        user = User(id=id, username=username, password=password)
        init_database.add(user)
        init_database.commit()
        return user
    return _add_user
