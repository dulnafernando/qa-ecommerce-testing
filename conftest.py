import re
from pathlib import Path
import pytest

SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Pytest hook executed for each phase of a test (setup, call, teardown).

    When a test execution ('call' phase) results in a failure, this hook checks
    whether a Playwright 'page' fixture was active. If present, it captures a
    full-page diagnostic screenshot and saves it with a sanitized filename to
    the screenshots/ directory.
    """
    outcome = yield
    report = outcome.get_result()

    # Capture visual evidence when the test call fails
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
            # Sanitize test name: parameterized tests produce characters like [, ], :, @
            # which can cause issues on Windows and CI artifact paths
            safe_name = re.sub(r"[^\w\-_\.]", "_", item.name)
            screenshot_path = SCREENSHOTS_DIR / f"{safe_name}.png"
            page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"\n[DIAGNOSTIC] Failure screenshot captured: {screenshot_path}")

            # Attach screenshot directly to the pytest-html report
            try:
                from pytest_html import extras

                extra = getattr(report, "extra", [])
                extra.append(extras.image(str(screenshot_path)))
                report.extra = extra
            except ImportError:
                pass


def pytest_html_report_title(report):
    """Sets a custom, professional title for the pytest-html execution report."""
    report.title = "Automation Exercise - QA Test Execution Report"


