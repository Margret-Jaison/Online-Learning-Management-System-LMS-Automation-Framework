class LoginPage:
    def __init__(self, page):
        self.page = page

    def open(self):
        self.page.goto("http://127.0.0.1:5000/login")

    def login(self, email, password):
        self.page.locator("input[name='email']").fill(email)
        self.page.locator("input[name='password']").fill(password)
        self.page.get_by_role("button", name="Login").click()
