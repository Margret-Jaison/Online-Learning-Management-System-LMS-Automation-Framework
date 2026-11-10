from pages.login_page import LoginPage
from utils.test_data import VALID_EMAIL, VALID_PASSWORD

def login(page):
    LoginPage(page).open()
    LoginPage(page).login(VALID_EMAIL, VALID_PASSWORD)

def test_enroll_in_course(browser_page):
    login(browser_page)
    browser_page.goto("http://127.0.0.1:5000/courses/1")
    browser_page.get_by_role("button", name="Enroll").click()
    assert browser_page.get_by_role("heading", name="Student Dashboard").is_visible()
    assert browser_page.get_by_text("Python Basics").is_visible()

def test_duplicate_enrollment_does_not_duplicate_course(browser_page):
    login(browser_page)
    for _ in range(2):
        browser_page.goto("http://127.0.0.1:5000/courses/2")
        browser_page.get_by_role("button", name="Enroll").click()
    browser_page.goto("http://127.0.0.1:5000/dashboard")
    assert browser_page.get_by_text("Java Fundamentals").count() == 1

def test_dashboard_shows_enrolled_courses(browser_page):
    login(browser_page)
    browser_page.goto("http://127.0.0.1:5000/courses/3")
    browser_page.get_by_role("button", name="Enroll").click()
    assert browser_page.get_by_text("Manual Testing").is_visible()
