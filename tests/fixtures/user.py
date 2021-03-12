import pytest
from common.confirm_email import generate_confirmation_token
from database import db
from models.user import User
from tests.fixtures.url import USERS_URL, CONFIRM_URL, LOGIN_URL


@pytest.fixture
def login(client):
    data = {
        "email": "mail@test.com",
        "password": "Testpassword@1"
    }
    response = client.post(LOGIN_URL, json=data)
    yield

@pytest.fixture
def setup_user(client):
    data = {
        "username": "test user",
        "email": "mail@test.com",
        "password": "Testpassword@1"
    }
    response = client.post(USERS_URL, json=data)
    conf_token = generate_confirmation_token(data['email'])
    response = client.get(CONFIRM_URL + conf_token)
    yield
    User.query.delete()
    db.session.commit()


@pytest.fixture
def teardown_user(client):
    yield
    User.query.delete()
    db.session.commit()
