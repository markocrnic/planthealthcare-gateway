import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '../app'))

from interface import app
from flask import json

token_for_testing = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmaXJzdF9uYW1lIjoiTWFya28iLCJsYXN0X25hbWUiOiJDcm5pYyIsInVzZXJuYW1lIjoibWNybmljIiwiZW1haWwiOiJtYXJrby5jcm5pY0BkZXZvdGVhbS5jb20iLCJhZG1pbiI6IlRydWUiLCJleHAiOjE4MzAyNDE0NTN9.qPE8YT0WkHDD6tcZ6_mkp3bIYwiXs-nR3HqDTBIDHS0"
jwt_header_auth = {'Authorization': 'Bearer ' + token_for_testing}

token_for_testing_expired = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmaXJzdF9uYW1lIjoiTWFya28iLCJsYXN0X25hbWUiOiJDcm5pYyIsInVzZXJuYW1lIjoibWNybmljIiwiZW1haWwiOiJtYXJrby5jcm5pY0BkZXZvdGVhbS5jb20iLCJhZG1pbiI6IlRydWUiLCJleHAiOjE1NzEwNDM5Mjd9.kAUOGll956ZNLK2ccg44RCvnxKlUuNABrtQLpwDU0io"
jwt_header_auth_expired = {'Authorization': 'Bearer ' + token_for_testing_expired}

token_for_testing_invalid = token_for_testing + 'a'
jwt_header_auth_invalid = {'Authorization': 'Bearer ' + token_for_testing_invalid}


# Test JWT token not present in headers
def test_jwt_token_not_present():
    response = app.test_client().get('/api/users/')

    assert response.status_code == 403


# Test invalid JWT token
def test_jwt_token_invalid():
    response = app.test_client().get('/api/users/', headers=jwt_header_auth_invalid)

    assert response.status_code == 401


# Test expired JWT token
def test_jwt_token_expired():
    response = app.test_client().get('/api/users/', headers=jwt_header_auth_expired)
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 401 and data == {'msg': 'JWT has expired.'}


# Test path not found
def test_path_not_found():
    response = app.test_client().get('/api/nonexistingroute/', headers=jwt_header_auth)
    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 404 and data == {'msg': 'Path not found'}


# Test GET all users successfully
def test_route_to_all_users_redirect_succsessful():
    response = app.test_client().get('/api/users/', headers=jwt_header_auth)

    assert response.status_code == 307


# Test GET one user successfully
def test_route_to_one_user_redirect_succsessful():
    response = app.test_client().get('/api/users/14', headers=jwt_header_auth)

    assert response.status_code == 307


# Test GET all flowers successfully
def test_route_to_all_flowers_redirect_succsessful():
    response = app.test_client().get('/api/flowers/', headers=jwt_header_auth)

    assert response.status_code == 307


# Test GET one flower successfully
def test_route_to_one_flower_redirect_succsessful():
    response = app.test_client().get('/api/flowers/14', headers=jwt_header_auth)

    assert response.status_code == 307


# Test GET all users2flowers successfully
def test_route_to_all_users2flowers_redirect_succsessful():
    response = app.test_client().get('/api/users2flowers/', headers=jwt_header_auth)

    assert response.status_code == 307


# Test GET one user2flower successfully
def test_route_to_one_user2flower_redirect_succsessful():
    response = app.test_client().get('/api/users2flowers/14', headers=jwt_header_auth)

    assert response.status_code == 307


# Test usermanagement adminlogin successfully
def test_usermanagement_adminlogin_redirect_succsessful():
    response = app.test_client().post('/api/usermanagement/adminlogin/', headers=jwt_header_auth, json={
        "username": "mcrnic",
        "password": "passwords"
    })

    assert response.status_code == 307


# Test usermanagement login successfully
def test_usermanagement_login_redirect_succsessful():
    response = app.test_client().post('/api/usermanagement/login/', headers=jwt_header_auth, json={
        "username": "mcrnic",
        "password": "passwords"
    })

    assert response.status_code == 307


# Test usermanagement register successfully
def test_usermanagement_register_succsessful():
    response = app.test_client().post('/api/usermanagement/register/', headers=jwt_header_auth, json={
        "username": "mcrnic",
        "password": "passwords",
        "email": "marko.crnic@devoteam.com"
    })

    assert response.status_code == 307
