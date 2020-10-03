import pytest
from resources.helpers.confirm_email import generate_confirmation_token
from database import db
from models.user import User as UserModel

@pytest.fixture
def user_token(client):
    data = {
        "email": "mail@test.com",
        "password": "Testpassword@1"
    }
    response = client.post("/login", json=data)
    token = 'Bearer ' + response.json['accessToken']
    yield token

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
