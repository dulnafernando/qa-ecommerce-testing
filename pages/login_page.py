from playwright.sync_api import Page


class LoginPage:
    """Encapsulates all interactions with the Login page."""

    URL = "https://automationexercise.com/login"

    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.locator('[data-qa="login-email"]')
        self.password_input = page.locator('[data-qa="login-password"]')
        self.login_button = page.locator('[data-qa="login-button"]')
        self.error_message = page.locator("text=Your email or password is incorrect!")

    def goto(self):
        self.page.goto(self.URL, wait_until="domcontentloaded", timeout=60000)

    def enter_email(self, email: str):
        self.email_input.fill(email)

    def enter_password(self, password: str):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

    def login(self, email: str, password: str):
        """Convenience method: performs a full login in one call."""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def is_logged_in(self) -> bool:
        return self.page.locator("text=Logged in as").is_visible()