class ProfilePage:
    def __init__(self, page):
        self.page = page

    def open(self):
        self.page.goto("http://127.0.0.1:5000/profile")

    def update_name(self, name):
        self.page.locator("input[name='name']").fill(name)
        self.page.get_by_role("button", name="Update Profile").click()
