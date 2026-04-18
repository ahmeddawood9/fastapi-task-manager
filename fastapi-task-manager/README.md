# FastAPI Task Manager Service

A high-performance, modular REST API built to manage task domain data. Designed with a clean, layered architecture that strictly separates routing, data validation, and database persistence layers to ensure maintainability and scalability.

## Tech Stack
* **Framework:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Data Validation:** Pydantic
* **Server:** Uvicorn (ASGI)

## Architecture
This project enforces domain boundaries using a modular directory structure, keeping database models isolated from API schemas:

```text
.
├── app/
│   ├── api/v1/endpoints/  # Route logic and dependency injection
│   ├── core/              # Global configuration and environment variables
│   ├── crud/              # Database operations
│   ├── models/            # SQLAlchemy database blueprints
│   ├── schemas/           # Pydantic data validation rules
│   ├── database.py        # PostgreSQL connection pool and session factory
│   └── main.py            # ASGI application entry point
├── tests/                 # Automated test suite
└── requirements.txt       # Project dependencies