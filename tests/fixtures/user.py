import pytest
from database import db
from models.user import User
from authz import Roles
from tests.fixtures.url import LOGIN_URL


@pytest.fixture
def login(client):
    data = {"email": "mail@test.com", "password": "Testpassword@1"}
    response = client.post(LOGIN_URL, json=data)
    yield


@pytest.fixture
def login_admin(client):
    data = {"email": "admin@test.com", "password": "Testpassword@2"}
    response = client.post(LOGIN_URL, json=data)
    yield


@pytest.fixture
def setup_user(client):
    data = {
        "username": "test user",
        "email": "mail@test.com",
        "password": "Testpassword@1",
    }
    user = User().create(data, autoconfirm=True)
    user.set_role(Roles.user)
    db.session.commit()
    yield
    user.delete()
    db.session.commit()


@pytest.fixture
def setup_admin_user(client):
    data = {
        "username": "test adminuser",
        "email": "admin@test.com",
        "password": "Testpassword@2",
    }
    user = User.create(data, autoconfirm=True)
    user.set_role(Roles.superadmin)
    db.session.commit()
    yield


@pytest.fixture
def teardown_user(client):
    yield
    User.query.delete()
    db.session.execute("DELETE FROM casbin_rule")
    db.session.commit()
