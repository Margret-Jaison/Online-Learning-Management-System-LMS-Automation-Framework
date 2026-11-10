from pages.courses_page import CoursesPage

def test_view_courses(browser_page):
    CoursesPage(browser_page).open()
    assert browser_page.get_by_role("heading", name="Courses").is_visible()
    assert browser_page.get_by_text("Python Basics").is_visible()

def test_search_course(browser_page):
    courses = CoursesPage(browser_page)
    courses.open()
    courses.search("Python")
    assert browser_page.get_by_text("Python Basics").is_visible()
    assert not browser_page.get_by_text("Java Fundamentals").is_visible()

def test_filter_by_category(browser_page):
    browser_page.goto("http://127.0.0.1:5000/courses?category=Testing")
    assert browser_page.get_by_text("Manual Testing").is_visible()
    assert not browser_page.get_by_text("Python Basics").is_visible()

def test_open_course_details(browser_page):
    browser_page.goto("http://127.0.0.1:5000/courses/1")
    assert browser_page.get_by_role("heading", name="Python Basics").is_visible()
    assert browser_page.get_by_role("button", name="Enroll").is_visible()
