import json

HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def test_password(client):
    data = {
        "username": "test user",
        "email": "passwordmail@test.com",
    }
    data['password'] = 'Password1@'
    response = client.post("/user", data=json.dumps(data), headers=HEADERS)
    assert response.status_code == 200

def test_password_whitespace(client):
    data = {
        "username": "test user1",
        "email": "passwordmail1@test.com",
    }
    data['password'] = 'Passwo rd1@'
    response = client.post("/user", data=json.dumps(data), headers=HEADERS)
    assert response.status_code == 400

def test_password_length(client):
    data = {
        "username": "test user2",
        "email": "passwordmail2@test.com",
    }
    data['password'] = 'Pword1@'
    response = client.post("/user", data=json.dumps(data), headers=HEADERS)
    assert response.status_code == 400

def test_password_uppercase(client):
    data = {
        "username": "test user3",
        "email": "passwordmail3@test.com",
    }
    data['password'] = 'password1@'
    response = client.post("/user", data=json.dumps(data), headers=HEADERS)
    assert response.status_code == 400

def test_password_number(client):
    data = {
        "username": "test user4",
        "email": "passwordmail4@test.com",
    }
    data['password'] = 'password@'
    response = client.post("/user", data=json.dumps(data), headers=HEADERS)
    assert response.status_code == 400

def test_password_symbol(client):
    data = {
        "username": "test user5",
        "email": "passwordmail5@test.com",
    }
    data['password'] = 'password1'
    response = client.post("/user", data=json.dumps(data), headers=HEADERS)
    assert response.status_code == 400
