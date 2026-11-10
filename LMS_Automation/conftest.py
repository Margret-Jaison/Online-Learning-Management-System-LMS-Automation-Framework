import os
import pytest
from playwright.sync_api import sync_playwright

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")

@pytest.fixture
def browser_page(request):
    """Start a browser, page and trace for one UI test."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()
        yield page

        # Save debugging files only when the test failed.
        report = getattr(request.node, "rep_call", None)
        if report and report.failed:
            os.makedirs("screenshots", exist_ok=True)
            page.screenshot(path=f"screenshots/{request.node.name}.png")
            context.tracing.stop(path=f"screenshots/{request.node.name}-trace.zip")
        else:
            context.tracing.stop()

        context.close()
        browser.close()

@pytest.fixture
def api_context():
    """Create an API request context for API tests."""
    with sync_playwright() as p:
        request = p.request.new_context(base_url=BASE_URL)
        yield request
        request.dispose()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)
