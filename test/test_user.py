import json

TOKEN = ''
HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def test_create_user(client):
    data = {
        "username": "test user",
        "email": "mail@test.com",
        "password": "testpassword"
    }
    response = client.post("/user", data=json.dumps(data), headers=HEADERS)
    global TOKEN
    TOKEN = 'Bearer ' + response.json['access_token']
    assert response.status_code == 200

def test_create_email_already_exists(client):
    data = {
        "username": "another user 1",
        "email": "mail@test.com",
        "password": "anotherpassword"
    }
    response = client.post("/user", data=json.dumps(data), headers=HEADERS)
    assert response.status_code == 409

def test_create_username_already_exists(client):
    data = {
        "username": "test user",
        "email": "mail2@test.com",
        "password": "anotherpassword"
    }
    response = client.post("/user", data=json.dumps(data), headers=HEADERS)
    assert response.status_code == 409

def test_create_user_no_email(client):
    data = {
        "username": "another user 2",
        "password": "testpassword"
    }
    response = client.post("/user", data=json.dumps(data), headers=HEADERS)
    assert response.status_code == 400

def test_create_user_null_email(client):
    data = {
        "username": "another user 3",
        "email": None,
        "password": "testpassword"
    }
    response = client.post("/user", data=json.dumps(data), headers=HEADERS)
    assert response.status_code == 400

def test_create_user_empty_email(client):
    data = {
        "username": "another user 4",
        "email": "",
        "password": "testpassword"
    }
    response = client.post("/user", data=json.dumps(data), headers=HEADERS)
    assert response.status_code == 400

def test_create_user_no_username(client):
    data = {
        "email": "mail3@test.com",
        "password": "testpassword"
    }
    response = client.post("/user", data=json.dumps(data), headers=HEADERS)
    assert response.status_code == 400

def test_create_user_null_username(client):
    data = {
        "username": None,
        "email": "mail4@test.com",
        "password": "testpassword"
    }
    response = client.post("/user", data=json.dumps(data), headers=HEADERS)
    assert response.status_code == 400

def test_create_user_no_password(client):
    data = {
        "username": "another user 5",
        "email": "mail5@test.com",
    }
    response = client.post("/user", data=json.dumps(data), headers=HEADERS)
    assert response.status_code == 400

def test_create_user_null_password(client):
    data = {
        "username": "another user 6",
        "email": "mail6@test.com",
        "password": None
    }
    response = client.post("/user", data=json.dumps(data), headers=HEADERS)
    assert response.status_code == 400

def test_create_user_whitespace_password(client):
    data = {
        "username": "another user 7",
        "email": "mail7@test.com",
        "password": 'whitespace in password'
    }
    response = client.post("/user", data=json.dumps(data), headers=HEADERS)
    assert response.status_code == 400

def test_get_user(client):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': TOKEN
    }
    response = client.get("/user/1", headers=headers)
    assert response.status_code == 200

def test_get_user_does_not_exist(client):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': TOKEN
    }
    response = client.get("/user/100", headers=headers)
    assert response.status_code == 404

def test_get_users(client):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': TOKEN
    }
    response = client.get("/user", headers=headers)
    assert response.status_code == 200

def test_delete_user_does_not_exist(client):
    headers = {
        'Authorization': TOKEN
    }
    response = client.delete("/user/100", headers=headers)
    assert response.status_code == 404

def test_delete_user(client):
    headers = {
        'Authorization': TOKEN
    }
    response = client.delete("/user/1", headers=headers)
    assert response.status_code == 200
