from playwright.sync_api import Page, expect
from pages.login_page import LoginPage


def test_valid_login(page: Page):
    """A registered user with correct credentials should log in successfully."""
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("tharindifernandi@gmail.com", "Ay@6ee2iDivYXms")

    expect(page.locator("text=Logged in as")).to_be_visible()


def test_invalid_password(page: Page):
    """An incorrect password should show an error and NOT log the user in."""
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login("tharindifernandi@gmail.com", "thar")

    expect(login_page.error_message).to_be_visible()