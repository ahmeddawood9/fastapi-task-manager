# FastAPI Task Manager API

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Tests](https://img.shields.io/badge/Tests-100%25-brightgreen?style=flat)](https://pytest.org)

A production-ready REST API built with FastAPI and PostgreSQL, demonstrating enterprise-grade backend architecture. This project emphasizes security, maintainability, and strict data validation, achieving 100% automated test coverage across all domain layers.

---

## Key Features

*   **Security First (Zero-Trust):** Implemented secure JWT-based OAuth2 authentication.
*   **Data Isolation:** Hard-enforced IDOR (Insecure Direct Object Reference) protection on all user-specific routes.
*   **Traffic Control:** Integrated IP-based rate limiting (SlowAPI) on authentication routes to mitigate brute-force attacks.
*   **Bulletproof Reliability:** 100% test coverage using Pytest and HTTPX with an isolated SQLite sandbox for testing.
*   **Clean Architecture:** Strict separation of concerns between SQLAlchemy models and Pydantic schemas.
*   **Modern Syntax:** Optimized for SQLAlchemy 2.0 and Pydantic V2 architecture.

---

## Tech Stack

*   **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Uvicorn ASGI)
*   **Database:** [PostgreSQL](https://www.postgresql.org/)
*   **ORM:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
*   **Migrations:** [Alembic](https://alembic.sqlalchemy.org/)
*   **Validation:** [Pydantic V2](https://docs.pydantic.dev/)
*   **Authentication:** JWT (JSON Web Tokens) & Passlib (Bcrypt)
*   **Testing:** Pytest & Pytest-cov

---

## Project Structure

```text
fastapi-task-manager/
├── alembic/                 # Version-controlled database migration scripts
├── app/                     
│   ├── api/v1/endpoints/    # Route definitions (Auth, Tasks)
│   ├── core/                # Security, JWT, and Rate limiting configurations
│   ├── crud/                # Isolated database transactions (CRUD)
│   ├── models/              # SQLAlchemy database blueprints
│   ├── schemas/             # Pydantic data validation rules
│   ├── database.py          # PostgreSQL connection & session factory
│   └── main.py              # ASGI application entry point
├── tests/                   # Automated test suite (100% Coverage)
├── alembic.ini              # Alembic configuration
├── requirements.txt         # Pinned dependency manifest
└── README.md
```

---

## Getting Started

### Prerequisites

*   Python 3.9+
*   PostgreSQL installed and running locally

### 1. Installation

Clone the repository and set up a virtual environment:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Configuration

The application connects to PostgreSQL. Ensure your credentials match those in `app/database.py`:

```python
# Default configuration:
SQLALCHEMY_DATABASE_URL = "postgresql://dawood_dev:learning123@localhost:5432/learning_db"
```

Apply database migrations:

```bash
alembic upgrade head
```

### 3. Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

*   **API URL:** `http://127.0.0.1:8000`
*   **Swagger UI (Docs):** `http://127.0.0.1:8000/docs`

---

## Testing & Coverage

To verify the test suite and ensure 100% coverage:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

The tests use an isolated SQLite in-memory database, ensuring that production/development data remains untouched.

---

## Security Highlights

*   **JWT Authentication:** Secure token-based access control.
*   **Rate Limiting:** Protects `/auth` endpoints from brute-force attempts.
*   **Input Validation:** Strict Pydantic models prevent malformed data injection.
*   **IDOR Protection:** Users can only access, modify, or delete their own tasks.
