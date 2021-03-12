import pytest
from common.confirm_email import generate_confirmation_token
from tests.fixtures.user import login, teardown_user, setup_user
from tests.fixtures.url import USERS_URL, CONFIRM_URL, LOGIN_URL

@pytest.mark.usefixtures('teardown_user')
def test_create_user(client):
    data = {
        "username": "test user",
        "email": "mail@test.com",
        "password": "Testpassword@1"
    }
    response = client.post(USERS_URL, json=data)
    conf_token = generate_confirmation_token(data['email'])
    response = client.get(CONFIRM_URL + conf_token)
    assert response.status_code == 200
    data = {
        "email": "mail@test.com",
        "password": "Testpassword@1"
    }
    response = client.post(LOGIN_URL, json=data)
    assert response.status_code == 200

@pytest.mark.usefixtures('setup_user')
class TestUser:
    def test_create_email_already_exists(self, client):
        data = {
            "username": "another user 1",
            "email": "mail@test.com",
            "password": "Anotherpassword@1"
        }
        response = client.post(USERS_URL, json=data)
        assert response.status_code == 409

    def test_create_username_already_exists(self, client):
        data = {
            "username": "test user",
            "email": "mail2@test.com",
            "password": "Anotherpassword@1"
        }
        response = client.post(USERS_URL, json=data)
        assert response.status_code == 409

    def test_create_user_no_email(self, client):
        data = {
            "username": "another user 2",
            "password": "Testpassword@1"
        }
        response = client.post(USERS_URL, json=data)
        assert response.status_code == 400

    def test_create_user_null_email(self, client):
        data = {
            "username": "another user 3",
            "email": None,
            "password": "Testpassword@1"
        }
        response = client.post(USERS_URL, json=data)
        assert response.status_code == 400

    def test_create_user_empty_email(self, client):
        data = {
            "username": "another user 4",
            "email": "",
            "password": "Testpassword@1"
        }
        response = client.post(USERS_URL, json=data)
        assert response.status_code == 400

    def test_create_user_no_username(self, client):
        data = {
            "email": "mail3@test.com",
            "password": "Testpassword@1"
        }
        response = client.post(USERS_URL, json=data)
        assert response.status_code == 400

    def test_create_user_null_username(self, client):
        data = {
            "username": None,
            "email": "mail4@test.com",
            "password": "Testpassword@1"
        }
        response = client.post(USERS_URL, json=data)
        assert response.status_code == 400

    def test_create_user_no_password(self, client):
        data = {
            "username": "another user 5",
            "email": "mail5@test.com",
        }
        response = client.post(USERS_URL, json=data)
        assert response.status_code == 400

    def test_create_user_null_password(self, client):
        data = {
            "username": "another user 6",
            "email": "mail6@test.com",
            "password": None
        }
        response = client.post(USERS_URL, json=data)
        assert response.status_code == 400

    def test_create_user_whitespace_password(self, client):
        data = {
            "username": "another user 7",
            "email": "mail7@test.com",
            "password": 'whitespace in password'
        }
        response = client.post(USERS_URL, json=data)
        assert response.status_code == 400


@pytest.mark.usefixtures('setup_user', 'login')
class TestUserGet:
    def test_get_user(self, client, login):
        response = client.get(f'{USERS_URL}/1')
        assert response.status_code == 200

    def test_get_user_does_not_exist(self, client, login):
        response = client.get(f'{USERS_URL}/100')
        assert response.status_code == 404

    def test_get_users(self, client, login):
        response = client.get(USERS_URL)
        assert response.status_code == 200

    def test_delete_user_does_not_exist(self, client, login):
        response = client.delete(f'{USERS_URL}/100')
        assert response.status_code == 404

    def test_delete_user(self, client, login):
        response = client.delete(f'{USERS_URL}/1')
        assert response.status_code == 200
