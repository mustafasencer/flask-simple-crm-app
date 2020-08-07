"""
    Created by Mustafa Sencer Özcan on 13.05.2020.
"""
import json
from os import environ

import pytest

import application

PASSWORD = '123'
REGISTER_RECORD = {
    "first_name": "trial",
    "last_name": "trial_surname",
    "email": "trial@blutv.com",
    "username": "trial",
    "password": PASSWORD
}
RESET_PASSWORD = {
    "new_password": "123123",
    "new_password_repeat": "123123"
}
ACCESS_TOKEN = None


@pytest.fixture(scope='module')
def client():
    environ.setdefault('MONGO_URI', 'mongodb://localhost:27017/local_blutv')
    environ.setdefault('REDIS_URL', 'redis://:password@localhost:6379/0')
    environ.setdefault('SECRET_KEY', '123123')
    return application.create_app().test_client(environ)


def test_register(client):
    mock_header = {
        'Content-Type': 'application/json'
    }
    mock_payload = json.dumps(REGISTER_RECORD)
    response = client.post('/contacts', data=mock_payload, headers=mock_header)
    assert response.status_code == 200


def test_get_all_contacts(client):
    mock_header = {
        'Content-Type': 'application/json'
    }
    response = client.get('/contacts', headers=mock_header)
    assert response.status_code == 200
    return response.json


def test_get_contact(client):
    mock_header = {
        'Content-Type': 'application/json'
    }
    contacts = test_get_all_contacts(client)
    _id = [row for row in contacts if row.get('email') == REGISTER_RECORD.get('email')][0].get('_id')
    response = client.get(f'/contacts/{_id}', headers=mock_header)
    assert response.status_code == 200
    return response.json


def test_login(client):
    contact = test_get_contact(client)
    mock_header = {
        'Content-Type': 'application/json'
    }
    mock_payload = json.dumps({
        "email": contact.get('email'),
        "password": PASSWORD
    })
    response = client.post('/login', data=mock_payload, headers=mock_header)
    assert response.status_code == 200
    global ACCESS_TOKEN
    ACCESS_TOKEN = response.json.get('access_token')


def test_reset_password(client):
    mock_header = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    mock_payload = json.dumps(RESET_PASSWORD)
    _id = test_get_contact(client).get('_id')
    response = client.post(f'/contacts/{_id}/reset-password', data=mock_payload, headers=mock_header)
    assert response.status_code == 200


def test_delete(client):
    mock_header = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    contact = test_get_contact(client)
    response = client.delete(f'/contacts/{contact.get("_id")}', headers=mock_header)
    assert response.status_code == 200
