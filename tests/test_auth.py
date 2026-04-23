# tests/test_auth.py

def test_register_user(client):
    """Test successful user registration."""
    response = client.post(
        "/auth/register",
        json={"email": "testuser@gmail.com", "password": "supersecurepassword"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "testuser@gmail.com"
    # Ensure the password isn't being returned in plain text!
    assert "password" not in response.json()

def test_register_duplicate_user(client):
    """Test that the API rejects duplicate emails."""
    # 1. Create the first user
    client.post(
        "/auth/register",
        json={"email": "clone@gmail.com", "password": "password123"}
    )
    
    # 2. Try to create the exact same user again
    response = client.post(
        "/auth/register",
        json={"email": "clone@gmail.com", "password": "password123"}
    )
    # The API should reject this request (usually a 400 Bad Request)
    assert response.status_code == 400

def test_login_success(client):
    """Test that valid credentials return a JWT token."""
    # 1. Register a user first
    client.post(
        "/auth/register",
        json={"email": "loginuser@gmail.com", "password": "mypassword"}
    )
    
    # 2. Attempt to log in (OAuth2 uses form data, not JSON!)
    response = client.post(
        "/auth/login",
        data={"username": "loginuser@gmail.com", "password": "mypassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password(client):
    """Test that incorrect credentials get rejected."""
    # 1. Register a user
    client.post(
        "/auth/register",
        json={"email": "secureuser@gmail.com", "password": "correctpassword"}
    )
    
    # 2. Try to log in with a bad password
    response = client.post(
        "/auth/login",
        data={"username": "secureuser@gmail.com", "password": "WRONGpassword"}
    )
    # The API should block them with a 401 Unauthorized
    assert response.status_code == 401