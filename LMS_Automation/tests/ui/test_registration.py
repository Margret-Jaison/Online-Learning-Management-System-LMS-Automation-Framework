import uuid

def test_registration_success(browser_page):
    browser_page.goto("http://127.0.0.1:5000/register")
    browser_page.locator("input[name='name']").fill("New Student")
    browser_page.locator("input[name='email']").fill(f"{uuid.uuid4().hex[:8]}@example.com")
    browser_page.locator("input[name='password']").fill("Pass12345")
    browser_page.get_by_role("button", name="Register").click()
    assert browser_page.locator("#message").inner_text() == "Registration successful"

def test_duplicate_registration(browser_page):
    browser_page.goto("http://127.0.0.1:5000/register")
    browser_page.locator("input[name='name']").fill("Student")
    browser_page.locator("input[name='email']").fill("student@example.com")
    browser_page.locator("input[name='password']").fill("Password123")
    browser_page.get_by_role("button", name="Register").click()
    assert browser_page.locator("#message").inner_text() == "Email already registered"

def test_registration_required_fields(browser_page):
    browser_page.goto("http://127.0.0.1:5000/register")
    assert browser_page.locator("input[name='name']").get_attribute("required") is not None
    assert browser_page.locator("input[name='email']").get_attribute("required") is not None
