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

def test_get_user(client):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': TOKEN
    }
    response = client.get("/user/1", headers=headers)
    assert response.status_code == 200

def test_get_users(client):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': TOKEN
    }
    response = client.get("/user", headers=headers)
    assert response.status_code == 200

def test_delete_user(client):
    headers = {
        'Authorization': TOKEN
    }
    response = client.delete("/user/1", headers=headers)
    assert response.status_code == 200
