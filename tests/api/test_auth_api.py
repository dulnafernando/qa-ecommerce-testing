import json
from pathlib import Path
import pytest
import requests

pytestmark = [pytest.mark.api]

BASE_URL = "https://automationexercise.com/api"
DATA_FILE = Path(__file__).parent.parent.parent / "test_data" / "login_data.json"

with open(DATA_FILE, encoding="utf-8") as f:
    login_cases = json.load(f)

VALID_USER = next(case for case in login_cases if case["case"] == "valid_login")


def test_verify_login_valid_credentials():
    """Verify POST /api/verifyLogin with valid credentials confirms user exists with responseCode 200."""
    response = requests.post(
        f"{BASE_URL}/verifyLogin",
        data={"email": VALID_USER["email"], "password": VALID_USER["password"]},
        timeout=10,
    )

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    data = response.json()
    assert data.get("responseCode") == 200, f"Expected payload responseCode 200, got {data.get('responseCode')}"
    assert data.get("message") == "User exists!"


def test_verify_login_invalid_credentials():
    """Negative test: POST /api/verifyLogin with unregistered user returns 404 User not found."""
    response = requests.post(
        f"{BASE_URL}/verifyLogin",
        data={"email": "nonexistent_qa_user_99999@example.com", "password": "WrongPassword123"},
        timeout=10,
    )

    assert response.status_code == 200, f"Expected HTTP 200 transport code, got {response.status_code}"
    data = response.json()
    assert data.get("responseCode") == 404, f"Expected payload responseCode 404, got {data.get('responseCode')}"
    assert data.get("message") == "User not found!"


def test_verify_login_missing_email_parameter():
    """Negative test: POST /api/verifyLogin without email returns 400 Bad Request."""
    response = requests.post(
        f"{BASE_URL}/verifyLogin",
        data={"password": VALID_USER["password"]},
        timeout=10,
    )

    assert response.status_code == 200, f"Expected HTTP 200 transport code, got {response.status_code}"
    data = response.json()
    assert data.get("responseCode") == 400, f"Expected payload responseCode 400, got {data.get('responseCode')}"
    assert "parameter is missing" in data.get("message", "")


def test_delete_verify_login_method_not_allowed():
    """Negative test: DELETE /api/verifyLogin must return 405 Method Not Supported."""
    response = requests.delete(f"{BASE_URL}/verifyLogin", timeout=10)

    assert response.status_code == 200, f"Expected HTTP 200 transport code, got {response.status_code}"
    data = response.json()
    assert data.get("responseCode") == 405, f"Expected payload responseCode 405, got {data.get('responseCode')}"
    assert data.get("message") == "This request method is not supported."


def test_get_user_detail_by_email_success():
    """Verify GET /api/getUserDetailByEmail retrieves account details for registered email."""
    response = requests.get(
        f"{BASE_URL}/getUserDetailByEmail",
        params={"email": VALID_USER["email"]},
        timeout=10,
    )

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    data = response.json()
    assert data.get("responseCode") == 200, f"Expected payload responseCode 200, got {data.get('responseCode')}"
    assert "user" in data, "Expected 'user' object in response"
    assert data["user"].get("email") == VALID_USER["email"]
