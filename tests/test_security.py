import pytest
from app.core.security import get_password_hash, verify_password

# --- FIXTURE ---
# A fixture is a setup function. Instead of typing "my_super_secret_password" 
# in every single test, we write it once here. Pytest will automatically 
# inject this data into any test that asks for "sample_password".
@pytest.fixture
def sample_password():
    return "my_super_secret_password"


# --- TESTS ---
# Pytest automatically finds and runs any function that starts with "test_"

def test_password_hashing(sample_password):
    """Test that hashing creates a string different from the original password."""
    hashed = get_password_hash(sample_password)
    
    # "assert" is the core of testing. It means "I expect this to be True. If it's False, fail the test."
    assert hashed != sample_password
    assert len(hashed) > 0

def test_password_verification_success(sample_password):
    """Test that a correct password successfully verifies against its hash."""
    hashed = get_password_hash(sample_password)
    
    is_valid = verify_password(sample_password, hashed)
    assert is_valid is True

def test_password_verification_fail(sample_password):
    """Test that a wrong password gets rejected."""
    hashed = get_password_hash(sample_password)
    wrong_password = "wrong_password_123"
    
    is_valid = verify_password(wrong_password, hashed)
    assert is_valid is False