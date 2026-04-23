import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# 1. Use an isolated SQLite database purely for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

# SQLite requires this specific engine argument
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- FIXTURES ---

@pytest.fixture(scope="session")
def test_db():
    """Builds the database tables before tests run, and destroys them after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def session(test_db):
    """Creates a fresh database session for a test."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    """
    Creates a FastAPI TestClient that intercepts database calls 
    and forces them into our SQLite test database.
    """
    def override_get_db():
        try:
            yield session
        finally:
            pass
            
    # Swap out the real database dependency for our test one
    app.dependency_overrides[get_db] = override_get_db
    
    # Yield the test client
    yield TestClient(app)
    
    # Clean up the override after the test finishes
    app.dependency_overrides.clear()