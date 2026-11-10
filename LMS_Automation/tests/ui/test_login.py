import pytest
from pages.login_page import LoginPage
from utils.test_data import VALID_EMAIL, VALID_PASSWORD

@pytest.mark.smoke
def test_valid_login(browser_page):
    login = LoginPage(browser_page)
    login.open()
    login.login(VALID_EMAIL, VALID_PASSWORD)
    assert "/dashboard" in browser_page.url
    assert browser_page.get_by_role("heading", name="Student Dashboard").is_visible()

@pytest.mark.parametrize("email,password", [
    ("wrong@example.com", "Password123"),
    ("student@example.com", "wrongpass"),
])
def test_invalid_login(browser_page, email, password):
    login = LoginPage(browser_page)
    login.open()
    login.login(email, password)
    assert browser_page.locator("#message").inner_text() == "Invalid email or password"

def test_empty_login_fields(browser_page):
    browser_page.goto("http://127.0.0.1:5000/login")
    assert browser_page.locator("input[name='email']").get_attribute("required") is not None
    assert browser_page.locator("input[name='password']").get_attribute("required") is not None

def test_login_page_has_register_link(browser_page):
    browser_page.goto("http://127.0.0.1:5000/login")
    assert browser_page.get_by_role("link", name="Register").is_visible()
