import pytest

# --- FIXTURE ---
@pytest.fixture
def auth_headers(client):
    """Registers a user, logs them in, and returns the JWT authorization header."""
    client.post("/auth/register", json={"email": "taskmaster@gmail.com", "password": "strongpassword"})
    response = client.post("/auth/login", data={"username": "taskmaster@gmail.com", "password": "strongpassword"})
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# --- TESTS ---

def test_create_task_unauthorized(client):
    """Prove that the Bouncer blocks requests with no token."""
    response = client.post("/tasks/", json={"title": "Sneaky task"})
    # 401 Unauthorized
    assert response.status_code == 401 

def test_create_task_authorized(client, auth_headers):
    """Prove that an authenticated user can create a task."""
    response = client.post("/tasks/", json={"title": "Buy Arch Linux stickers"}, headers=auth_headers)
    
    assert response.status_code == 201
    assert response.json()["title"] == "Buy Arch Linux stickers"
    # Ensure the database actually linked the task to a user
    assert response.json()["owner_id"] is not None

def test_read_own_tasks(client, auth_headers):
    """Prove that a user can fetch their own list of tasks."""
    # Create two tasks
    client.post("/tasks/", json={"title": "Task 1"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Task 2"}, headers=auth_headers)
    
    response = client.get("/tasks/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 2

def test_idor_protection_delete(client, auth_headers):
    """
    THE ULTIMATE TEST: Prove User B cannot delete User A's task.
    """
    # 1. User A (auth_headers) creates a task
    task_response = client.post("/tasks/", json={"title": "User A's Secret Task"}, headers=auth_headers)
    task_id = task_response.json()["id"]

    # 2. Create User B (The Hacker) and get their token
    client.post("/auth/register", json={"email": "hacker@gmail.com", "password": "hackerpassword"})
    login_resp = client.post("/auth/login", data={"username": "hacker@gmail.com", "password": "hackerpassword"})
    
    hacker_token = login_resp.json()["access_token"]
    hacker_headers = {"Authorization": f"Bearer {hacker_token}"}

    # 3. User B attempts to delete User A's task
    delete_response = client.delete(f"/tasks/{task_id}", headers=hacker_headers)
    
    # 4. The API should say "Not Found" (404) because the IDOR filter blocked it!
    assert delete_response.status_code == 404

def test_read_task(client, auth_headers):
    """Test reading a single task."""
    task_response = client.post("/tasks/", json={"title": "Single Task"}, headers=auth_headers)
    task_id = task_response.json()["id"]

    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Single Task"

def test_read_task_not_found(client, auth_headers):
    """Test reading a task that doesn't exist."""
    response = client.get("/tasks/9999", headers=auth_headers)
    assert response.status_code == 404

def test_update_task(client, auth_headers):
    """Test updating a task."""
    task_response = client.post("/tasks/", json={"title": "Old Title"}, headers=auth_headers)
    task_id = task_response.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"title": "New Title"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"

def test_update_task_not_found(client, auth_headers):
    """Test updating a task that doesn't exist."""
    response = client.put("/tasks/9999", json={"title": "New Title"}, headers=auth_headers)
    assert response.status_code == 404

def test_delete_task_success(client, auth_headers):
    """Test deleting a task successfully."""
    task_response = client.post("/tasks/", json={"title": "Delete Me"}, headers=auth_headers)
    task_id = task_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204
    
    # Verify it's gone
    get_response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_response.status_code == 404