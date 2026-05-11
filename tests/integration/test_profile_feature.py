import requests
from uuid import uuid4


def register_and_login(base_url, username_suffix="profile"):
    unique_id = str(uuid4()).replace("-", "")[:8]

    user_data = {
        "first_name": "Profile",
        "last_name": "Tester",
        "email": f"profile{unique_id}@example.com",
        "username": f"profile{unique_id}",
        "password": "SecurePass123!",
        "confirm_password": "SecurePass123!"
    }

    register_response = requests.post(
        f"{base_url}/auth/register",
        json=user_data
    )

    assert register_response.status_code == 201

    login_response = requests.post(
        f"{base_url}/auth/login",
        json={
            "username": user_data["username"],
            "password": user_data["password"]
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "token": token,
        "user_data": user_data
    }


def test_get_profile(fastapi_server):
    base_url = fastapi_server.rstrip("/")

    auth = register_and_login(base_url)

    headers = {
        "Authorization": f"Bearer {auth['token']}"
    }

    response = requests.get(
        f"{base_url}/profile",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == auth["user_data"]["username"]
    assert data["email"] == auth["user_data"]["email"]


def test_update_profile(fastapi_server):
    base_url = fastapi_server.rstrip("/")

    auth = register_and_login(base_url)

    headers = {
        "Authorization": f"Bearer {auth['token']}"
    }

    updated_data = {
        "username": "updateduser",
        "email": "updated@example.com",
        "first_name": "Updated",
        "last_name": "User"
    }

    response = requests.put(
        f"{base_url}/profile",
        json=updated_data,
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "updateduser"
    assert data["email"] == "updated@example.com"


def test_change_password(fastapi_server):
    base_url = fastapi_server.rstrip("/")

    auth = register_and_login(base_url)

    headers = {
        "Authorization": f"Bearer {auth['token']}"
    }

    response = requests.post(
        f"{base_url}/profile/change-password",
        json={
            "current_password": "SecurePass123!",
            "new_password": "NewSecurePass123!",
            "confirm_new_password": "NewSecurePass123!"
        },
        headers=headers
    )

    assert response.status_code == 200

    login_response = requests.post(
        f"{base_url}/auth/login",
        json={
            "username": auth["user_data"]["username"],
            "password": "NewSecurePass123!"
        }
    )

    assert login_response.status_code == 200


def test_change_password_wrong_current_password(fastapi_server):
    base_url = fastapi_server.rstrip("/")

    auth = register_and_login(base_url)

    headers = {
        "Authorization": f"Bearer {auth['token']}"
    }

    response = requests.post(
        f"{base_url}/profile/change-password",
        json={
            "current_password": "WrongPassword123!",
            "new_password": "NewSecurePass123!",
            "confirm_new_password": "NewSecurePass123!"
        },
        headers=headers
    )

    assert response.status_code == 400