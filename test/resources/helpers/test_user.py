import pytest
from test.fixtures.user import teardown_user
from test.fixtures.url import USERS_URL

@pytest.mark.usefixtures('teardown_user')
class TestHelper:
    def test_password(self, client):
        data = {
            "username": "test user",
            "email": "passwordmail@test.com",
        }
        data['password'] = 'Password1@'
        response = client.post(USERS_URL, json=data)
        assert response.status_code == 200

    def test_password_whitespace(self, client):
        data = {
            "username": "test user1",
            "email": "passwordmail1@test.com",
        }
        data['password'] = 'Passwo rd1@'
        response = client.post(USERS_URL, json=data)
        assert response.status_code == 400

    def test_password_length(self, client):
        data = {
            "username": "test user2",
            "email": "passwordmail2@test.com",
        }
        data['password'] = 'Pword1@'
        response = client.post(USERS_URL, json=data)
        assert response.status_code == 400

    def test_password_uppercase(self, client):
        data = {
            "username": "test user3",
            "email": "passwordmail3@test.com",
        }
        data['password'] = 'password1@'
        response = client.post(USERS_URL, json=data)
        assert response.status_code == 400

    def test_password_number(self, client):
        data = {
            "username": "test user4",
            "email": "passwordmail4@test.com",
        }
        data['password'] = 'password@'
        response = client.post(USERS_URL, json=data)
        assert response.status_code == 400

    def test_password_symbol(self, client):
        data = {
            "username": "test user5",
            "email": "passwordmail5@test.com",
        }
        data['password'] = 'password1'
        response = client.post(USERS_URL, json=data)
        assert response.status_code == 400
