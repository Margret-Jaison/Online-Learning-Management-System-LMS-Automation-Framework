from pages.login_page import LoginPage
from utils.test_data import VALID_EMAIL, VALID_PASSWORD

def test_update_profile_name(browser_page):
    login = LoginPage(browser_page)
    login.open()
    login.login(VALID_EMAIL, VALID_PASSWORD)
    browser_page.goto("http://127.0.0.1:5000/profile")
    browser_page.locator("input[name='name']").fill("Updated Student")
    browser_page.get_by_role("button", name="Update Profile").click()
    assert browser_page.locator("#message").inner_text() == "Profile updated"

def test_logout(browser_page):
    login = LoginPage(browser_page)
    login.open()
    login.login(VALID_EMAIL, VALID_PASSWORD)
    browser_page.goto("http://127.0.0.1:5000/logout")
    assert "/login" in browser_page.url

def test_navigation_to_courses(browser_page):
    browser_page.goto("http://127.0.0.1:5000/")
    browser_page.get_by_role("link", name="Courses").click()
    assert "/courses" in browser_page.url
