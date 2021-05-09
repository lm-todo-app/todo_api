import pytest
from common.confirm_email import generate_confirmation_token
from tests.fixtures.user import login
from tests.fixtures.user import teardown_user
from tests.fixtures.user import setup_user
from tests.fixtures.url import USERS_URL
from tests.fixtures.url import CONFIRM_URL
from tests.fixtures.url import LOGIN_URL
from tests.fixtures.url import TOKEN_URL


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

    def test_delete_self_logout(self, client, login):
        response = client.delete(f'{USERS_URL}/1')
        assert response.status_code == 200
        response = client.get(f'{USERS_URL}')
        assert response.status_code == 401

    def test_update_username(self, client, login):
        data = {
            "username": "updated user",
            "email": "mail@test.com",
        }
        response = client.put(f'{USERS_URL}/1', json=data)
        assert response.status_code == 200
        assert response.json['data']['username'] == 'updated user'

    def test_update_email(self, client, login):
        data = {
            "username": "test user",
            "email": "updated_mail@test.com",
        }
        response = client.put(f'{USERS_URL}/1', json=data)
        assert response.status_code == 200
        assert response.json['data']['email'] == 'updated_mail@test.com'

    def test_update_password(self, client, login):
        data = {
            "username": "test user",
            "email": "mail@test.com",
            "password": "Updatedpassword@1"
        }
        response = client.put(f'{USERS_URL}/1', json=data)
        assert response.status_code == 200
        response = client.post(f'{TOKEN_URL}/remove')
        data = {
            "email": "mail@test.com",
            "password": "Testpassword@1"
        }
        response = client.post(LOGIN_URL, json=data)
        assert response.status_code == 401
        data = {
            "email": "mail@test.com",
            "password": "Updatedpassword@1"
        }
        response = client.post(LOGIN_URL, json=data)
        assert response.status_code == 200
