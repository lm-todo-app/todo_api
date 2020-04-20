import json

TOKEN = ''

def test_create_user(client):
    data = {
        "username": "test user",
        "email": "mail@test.com",
        "password": "testpassword"
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = client.post("/user", data=json.dumps(data), headers=headers)
    global TOKEN
    TOKEN = 'Bearer ' + response.json[0]['access_token']
    assert response.status_code == 200

def test_create_user_already_exists(client):
    data = {
        "username": "another user",
        "email": "mail@test.com",
        "password": "anotherpassword"
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = client.post("/user", data=json.dumps(data), headers=headers)
    assert response.status_code == 500

def test_create_user_no_email(client):
    data = {
        "username": "test user",
        "password": "testpassword"
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = client.post("/user", data=json.dumps(data), headers=headers)
    assert response.status_code == 500

def test_create_user_empty_email(client):
    data = {
        "username": "test user",
        "email": None,
        "password": "testpassword"
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = client.post("/user", data=json.dumps(data), headers=headers)
    assert response.status_code == 500

def test_create_user_no_username(client):
    data = {
        "email": "mail2@test.com",
        "password": "testpassword"
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = client.post("/user", data=json.dumps(data), headers=headers)
    assert response.status_code == 500

def test_create_user_empty_username(client):
    data = {
        "username": None,
        "email": "mail2@test.com",
        "password": "testpassword"
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = client.post("/user", data=json.dumps(data), headers=headers)
    assert response.status_code == 500

def test_create_user_no_password(client):
    data = {
        "username": "test user",
        "email": "mail3@test.com",
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = client.post("/user", data=json.dumps(data), headers=headers)
    assert response.status_code == 500

def test_create_user_empty_password(client):
    data = {
        "username": "test user",
        "email": "mail4@test.com",
        "password": None
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = client.post("/user", data=json.dumps(data), headers=headers)
    assert response.status_code == 500

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
