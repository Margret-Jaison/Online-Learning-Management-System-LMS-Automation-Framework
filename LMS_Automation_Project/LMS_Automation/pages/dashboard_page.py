class DashboardPage:
    def __init__(self, page):
        self.page = page

    def open(self):
        self.page.goto("http://127.0.0.1:5000/dashboard")
