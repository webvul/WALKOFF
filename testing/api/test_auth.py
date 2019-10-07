import json
import logging
from http import HTTPStatus

import yaml
from starlette.testclient import TestClient

from testing.api.helpers import assert_crud_resource

logger = logging.getLogger(__name__)

base_auth_url = "/walkoff/api/auth/"


def test_super_admin_login(api: TestClient):
    admin_data = {
        "username": "super_admin",
        "password": "super_admin"
    }
    p = api.post(f"{base_auth_url + 'login'}", data=json.dumps(admin_data))
    assert p.status_code == 201
    p_response = p.json()
    assert p_response["access_token"]
    assert p_response["refresh_token"]

    return p_response


def test_invalid_super_admin_login(api: TestClient):
    admin_data = {
        "username": "super_admin",
        "password": "incorrect_password"
    }
    p = api.post(f"{base_auth_url + 'login'}", data=json.dumps(admin_data))
    assert p.status_code == 401


def test_admin_login(api: TestClient):
    admin_data = {
        "username": "admin",
        "password": "admin"
    }
    p = api.post(f"{base_auth_url + 'login'}", data=json.dumps(admin_data))
    assert p.status_code == 201
    p_response = p.json()
    assert p_response["access_token"]
    assert p_response["refresh_token"]

    return p_response


def test_invalid_admin_login(api: TestClient):
    admin_data = {
        "username": "admin",
        "password": "incorrect_password"
    }
    p = api.post(f"{base_auth_url + 'login'}", data=json.dumps(admin_data))
    assert p.status_code == 401


def test_admin_refresh(api: TestClient):
    tokens = test_admin_login(api)
    refresh_token = tokens["refresh_token"]
    headers = {"Authorization":  "Bearer " + refresh_token}

    p = api.post(f"{base_auth_url + 'refresh'}", headers=headers)
    assert p.status_code == 200
    p_response = p.json()
    assert p_response["access_token"]


def test_invalid_admin_refresh(api: TestClient):
    tokens = test_admin_login(api)
    invalid_token = tokens["access_token"]
    headers = {"Authorization":  "Bearer " + invalid_token}

    p = api.post(f"{base_auth_url + 'refresh'}", headers=headers)
    assert p.status_code == 400


def test_admin_logout(api: TestClient):
    tokens = test_admin_login(api)
    headers = {"Authorization":  "Bearer " + tokens["access_token"]}
    data = {"refresh_token": tokens["refresh_token"]}

    p = api.post(f"{base_auth_url + 'logout'}", headers=headers, data=json.dumps(data))
    assert p.status_code == 204


