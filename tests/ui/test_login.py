import json
from pathlib import Path

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage

DATA_FILE = Path(__file__).parent.parent.parent / "test_data" / "login_data.json"

with open(DATA_FILE, encoding="utf-8") as f:
    login_cases = json.load(f)


@pytest.mark.parametrize(
    "case_data",
    login_cases,
    ids=[case["case"] for case in login_cases],
)
def test_login(page: Page, case_data):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(case_data["email"], case_data["password"])

    if case_data["expected"] == "success":
        assert login_page.is_logged_in(), f"Expected login to succeed for case '{case_data['case']}'"
    else:
        assert not login_page.is_logged_in(), f"Expected login to fail for case '{case_data['case']}'"