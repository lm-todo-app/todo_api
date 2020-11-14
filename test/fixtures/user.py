import pytest
from resources.helpers.confirm_email import generate_confirmation_token
from database import db
from models.user import User as UserModel
from test.fixtures.url import USERS_URL, CONFIRM_URL, LOGIN_URL

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
    UserModel.query.delete()
    db.session.commit()


@pytest.fixture
def teardown_user(client):
    yield
    UserModel.query.delete()
    db.session.commit()
