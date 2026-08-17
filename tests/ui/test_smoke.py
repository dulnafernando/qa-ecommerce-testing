from playwright.sync_api import Page


def test_homepage_loads(page: Page):
    """Sanity check: confirms Playwright + pytest are wired up correctly."""
    page.goto("https://automationexercise.com")
    assert "Automation Exercise" in page.title()