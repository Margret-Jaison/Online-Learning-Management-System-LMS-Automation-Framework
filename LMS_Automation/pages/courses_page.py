class CoursesPage:
    def __init__(self, page):
        self.page = page

    def open(self):
        self.page.goto("http://127.0.0.1:5000/courses")

    def search(self, text):
        self.page.locator("input[name='q']").fill(text)
        self.page.get_by_role("button", name="Search").click()
