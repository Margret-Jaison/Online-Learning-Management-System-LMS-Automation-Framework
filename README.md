# Online Learning Management System (LMS) - Automation Framework

A beginner-friendly sample project using Python, Playwright, Pytest and Page Object Model.

## 1. What is included?

- Small demo LMS website and REST API (`app.py`)
- 15+ UI test scenarios
- 8 API test scenarios
- Page Object Model classes in `pages/`
- Reusable fixtures in `conftest.py`
- Data-driven login tests using `pytest.mark.parametrize`
- `smoke`, `regression` and `api` markers
- HTML report
- Screenshot capture for failed UI tests
- GitHub Actions workflow
- Optional parallel and retry commands

## 2. Install and run

Use Python 3.10 or newer. Open a terminal in this project folder.

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

Install packages and browser:
```bash
pip install -r requirements.txt
playwright install chromium
```

Start the demo LMS in Terminal 1:
```bash
python app.py
```
Keep this terminal running. Open http://127.0.0.1:5000 in your browser.

## 3. Run tests

Open Terminal 2 in the project folder.

Run all tests:
```bash
pytest
```

Run only UI tests:
```bash
pytest tests/ui
```

Run only API tests:
```bash
pytest tests/api
```

Run smoke tests:
```bash
pytest -m smoke
```

Run API marker tests:
```bash
pytest -m api
```

Run in parallel (4 workers):
```bash
pytest -n 4
```

Retry failed tests once:
```bash
pytest --reruns 1
```

The HTML report is created at `reports/report.html`. Create the `reports` folder before the first run if it does not exist.

## 4. Important notes

- This is a learning/demo LMS, not a production application.
- The assignment did not provide a real LMS URL or API documentation, so this project includes a small local demo app.
- The sample UI tests use simple CSS locators and Playwright role locators.
- The profile page demonstrates updating a student's name. Email/password changes are not implemented in the demo.
- The demo app stores data in memory. Restarting `app.py` resets the data.
- For a real LMS, update the base URL and locators in the page classes and use the real API endpoints and request fields.
- UI tests are independent in browser state, but the demo app's in-memory data is shared while it is running. If running tests in parallel, avoid tests that modify the same data at the same time.

## 5. Project structure

```text
LMS_Automation/
├── app.py
├── tests/
│   ├── ui/
│   │   ├── test_login.py
│   │   ├── test_registration.py
│   │   ├── test_courses.py
│   │   ├── test_enrollment.py
│   │   └── test_profile.py
│   └── api/
│       └── test_courses_api.py
├── pages/
│   ├── login_page.py
│   ├── courses_page.py
│   ├── dashboard_page.py
│   └── profile_page.py
├── utils/
│   └── test_data.py
├── reports/
├── screenshots/
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## 6. Demo login

Email: `student@example.com`  
Password: `Password123`

## 7. GitHub

```bash
git init
git add .
git commit -m "Add LMS Playwright automation framework"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```
