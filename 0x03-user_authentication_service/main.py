#!/usr/bin/env python3
"""main app for integration off app.py"""

import requests
from app import AUTH

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """registers a new user"""
    response = requests.post(
            f"{BASE_URL}/users", data={"email": email, "password": password})
    assert response.status_code == 200, (
            f"Registrarion failed:{response.status_code} - {response.text}")


def log_in_wrong_password(email: str, password: str) -> None:
    """wrong password login attempt"""
    response = requests.post(
            f"{BASE_URL}/sessions", data={"email": email, "password": password}
    )
    assert response.status_code == 401, (
            f"Failed to log in with wrong password:"
            f"{response.status_code} - {response.text}")


def log_in(email: str, password: str) -> str:
    """Log in and return the session ID"""
    response = requests.post(
            f"{BASE_URL}/sessions",
            data={"email": email, "password": password}
    )
    assert response.status_code == 200, (
        f"Log in failed: "
        f"{response.status_code} - {response.text}"
    )
    return response.cookies["session_id"]


def profile_unlogged() -> None:
    """Access the profile without logging in"""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, (
            f"Accessed profile: "
            f"{response.status_code} - {response.text}"
    )


def profile_logged(session_id: str) -> None:
    """Access the profile while logged in"""
    cookies = {"session_id": session_id}
    response = requests.get(
            f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200, (
        f"Failed to access profile while logged in: "
        f"{response.status_code} - {response.text}"
    )


def log_out(session_id: str) -> None:
    """Log out the user session"""
    cookies = {"session_id": session_id}
    response = requests.delete(
            f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200, (
            f"Failed to log out: "
            f"{response.status_code} - {response.text}"
    )


def reset_password_token(email: str) -> str:
    """Request a password reset token"""
    response = requests.post(
            f"{BASE_URL}/reset_password", data={"email": email})
    assert response.status_code == 200, (
            f"Failed to request reset token: "
            f"{response.status_code} - {response.text}"
    )
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the password using the reset token"""
    response = requests.put(f"{BASE_URL}/reset_password", data={
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    })
    assert response.status_code == 200, (
            f"Failed to update password: "
            f"{response.status_code} - {response.text}"
    )


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
