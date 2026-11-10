from flask import Flask, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = "learning-lms-secret"

courses = [
    {"id": 1, "title": "Python Basics", "category": "Programming", "description": "Learn Python from the beginning."},
    {"id": 2, "title": "Java Fundamentals", "category": "Programming", "description": "Learn core Java concepts."},
    {"id": 3, "title": "Manual Testing", "category": "Testing", "description": "Learn software testing basics."},
]
users = {"student@example.com": {"name": "Demo Student", "password": "Password123"}}
enrollments = []

def page(content):
    return f"""<!doctype html><html><head><title>Simple LMS</title>
    <style>body{{font-family:Arial;margin:35px;max-width:850px}} input,select{{padding:8px;margin:5px}}
    button{{padding:8px 14px;margin:5px}} a{{margin-right:12px}}</style></head><body>
    <nav><a href="/">Home</a><a href="/courses">Courses</a><a href="/dashboard">Dashboard</a>
    <a href="/profile">Profile</a><a href="/logout">Logout</a></nav><hr>{content}</body></html>"""

@app.route("/")
def home():
    return page("<h1>Online Learning Management System</h1><p>Welcome to the demo LMS.</p><a href='/login'>Login</a>")

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        email, password = request.form.get("email", ""), request.form.get("password", "")
        if email in users and users[email]["password"] == password:
            session["email"] = email
            return redirect("/dashboard")
        message = "<p id='message'>Invalid email or password</p>"
    return page(f"""<h1>Login</h1>{message}<form method="post">
    <label>Email</label><input name="email" type="email" required>
    <label>Password</label><input name="password" type="password" required>
    <button type="submit">Login</button></form><a href="/register">Register</a>""")

@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        name, email, password = request.form.get("name",""), request.form.get("email",""), request.form.get("password","")
        if email in users:
            message = "<p id='message'>Email already registered</p>"
        elif name and email and password:
            users[email] = {"name": name, "password": password}
            message = "<p id='message'>Registration successful</p>"
    return page(f"""<h1>Registration</h1>{message}<form method="post">
    <label>Name</label><input name="name" required><label>Email</label><input name="email" type="email" required>
    <label>Password</label><input name="password" type="password" required><button>Register</button></form>""")

@app.route("/courses")
def course_list():
    q = request.args.get("q", "").lower()
    category = request.args.get("category", "")
    visible = [c for c in courses if q in c["title"].lower() and (not category or c["category"] == category)]
    items = "".join(f"<li><a href='/courses/{c['id']}'>{c['title']}</a> - {c['category']}</li>" for c in visible)
    return page(f"""<h1>Courses</h1><form><input name='q' placeholder='Search courses'>
    <select name='category'><option value=''>All</option><option>Programming</option><option>Testing</option></select>
    <button>Search</button></form><ul>{items}</ul>""")

@app.route("/courses/<int:course_id>")
def course_detail(course_id):
    c = next((x for x in courses if x["id"] == course_id), None)
    if not c: return "Course not found", 404
    return page(f"<h1>{c['title']}</h1><p>{c['description']}</p><form method='post' action='/enroll/{course_id}'><button>Enroll</button></form>")

@app.route("/enroll/<int:course_id>", methods=["POST"])
def enroll(course_id):
    email = session.get("email")
    if not email: return redirect("/login")
    if not any(e["email"] == email and e["course_id"] == course_id for e in enrollments):
        enrollments.append({"email": email, "course_id": course_id, "progress": 0})
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    email = session.get("email")
    if not email: return redirect("/login")
    enrolled = [e for e in enrollments if e["email"] == email]
    names = [next((c["title"] for c in courses if c["id"] == e["course_id"]), "Unknown") for e in enrolled]
    items = "".join(f"<li>{name}</li>" for name in names) or "<li>No enrolled courses</li>"
    return page(f"<h1>Student Dashboard</h1><p>Welcome, {users[email]['name']}</p><h2>My Courses</h2><ul>{items}</ul><p>Progress: 0%</p>")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    email = session.get("email")
    if not email: return redirect("/login")
    message = ""
    if request.method == "POST":
        users[email]["name"] = request.form.get("name", users[email]["name"])
        message = "<p id='message'>Profile updated</p>"
    return page(f"""<h1>Profile</h1>{message}<form method='post'>
    <label>Name</label><input name='name' value="{users[email]['name']}" required>
    <label>Email</label><input value='{email}' disabled><button>Update Profile</button></form>""")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# Simple REST API used by the API automation tests
@app.route("/api/courses", methods=["GET", "POST"])
def api_courses():
    if request.method == "GET":
        return jsonify(courses), 200
    data = request.get_json(silent=True) or {}
    if not data.get("title") or not data.get("category"):
        return jsonify({"error": "title and category are required"}), 400
    new_course = {"id": max([c["id"] for c in courses], default=0) + 1,
                  "title": data["title"], "category": data["category"],
                  "description": data.get("description", "")}
    courses.append(new_course)
    return jsonify(new_course), 201

@app.route("/api/courses/<int:course_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def api_course(course_id):
    course = next((c for c in courses if c["id"] == course_id), None)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    if request.method == "GET":
        return jsonify(course), 200
    if request.method in ["PUT", "PATCH"]:
        data = request.get_json(silent=True) or {}
        if request.method == "PUT" and (not data.get("title") or not data.get("category")):
            return jsonify({"error": "title and category are required"}), 400
        for key in ["title", "category", "description"]:
            if key in data: course[key] = data[key]
        return jsonify(course), 200
    courses.remove(course)
    return "", 204

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
