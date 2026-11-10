import uuid
import pytest

@pytest.mark.api
def test_get_all_courses(api_context):
    response = api_context.get("/api/courses")
    assert response.status == 200
    assert isinstance(response.json(), list)

@pytest.mark.api
def test_get_course_by_id(api_context):
    response = api_context.get("/api/courses/1")
    assert response.status == 200
    assert response.json()["title"] == "Python Basics"

@pytest.mark.api
def test_create_course(api_context):
    data = {"title": "API " + uuid.uuid4().hex[:6], "category": "Testing"}
    response = api_context.post("/api/courses", data=data)
    assert response.status == 201
    assert response.json()["title"] == data["title"]

@pytest.mark.api
def test_update_course(api_context):
    response = api_context.put("/api/courses/1", data={
        "title": "Python Basics Updated", "category": "Programming"
    })
    assert response.status == 200
    assert response.json()["title"] == "Python Basics Updated"

@pytest.mark.api
def test_partial_update_course(api_context):
    response = api_context.patch("/api/courses/2", data={"description": "Updated description"})
    assert response.status == 200
    assert response.json()["description"] == "Updated description"

@pytest.mark.api
def test_delete_course(api_context):
    created = api_context.post("/api/courses", data={
        "title": "Delete Me", "category": "Testing"
    })
    course_id = created.json()["id"]
    response = api_context.delete(f"/api/courses/{course_id}")
    assert response.status == 204

@pytest.mark.api
def test_get_invalid_course(api_context):
    response = api_context.get("/api/courses/99999")
    assert response.status == 404
    assert response.json()["error"] == "Course not found"

@pytest.mark.api
def test_create_course_with_invalid_data(api_context):
    response = api_context.post("/api/courses", data={"title": ""})
    assert response.status == 400
    assert "error" in response.json()
