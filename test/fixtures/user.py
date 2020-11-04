import pytest
from resources.helpers.confirm_email import generate_confirmation_token
from database import db
from models.user import User as UserModel
from http.cookies import SimpleCookie

@pytest.fixture
def login(client):
    data = {
        "email": "mail@test.com",
        "password": "Testpassword@1"
    }
    response = client.post("/login", json=data)
    yield

@pytest.fixture
def setup_user(client):
    data = {
        "username": "test user",
        "email": "mail@test.com",
        "password": "Testpassword@1"
    }
    response = client.post("/users", json=data)
    conf_token = generate_confirmation_token(data['email'])
    response = client.get('/confirm/' + conf_token)
    yield
    UserModel.query.delete()
    db.session.commit()


@pytest.fixture
def teardown_user(client):
    yield
    UserModel.query.delete()
    db.session.commit()
