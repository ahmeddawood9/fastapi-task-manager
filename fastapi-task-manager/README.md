# FastAPI Task Manager 

A production-ready Task Management API built with FastAPI. This project serves as a practical implementation of my journey through Backend Engineering and DevOps.


- [x] **Week 1: FastAPI Basics** (Current)
  - [x] In-memory CRUD operations
  - [x] Pydantic data validation
  - [x] Structured routing (APIRouter)
- [ ] **Week 2: Persistence (PostgreSQL + SQLAlchemy)**
- [ ] **Week 3: Authentication (JWT)**
- [ ] **Week 4: Automated Testing (Pytest)**
- [ ] **Week 5: DevOps & CI/CD (Docker + GitHub Actions)**
- [ ] **Week 6-8: Scaling & Advanced Features**

---

##  Project Structure
Following a clean, layered architecture to ensure scalability:

```text
.
├── app/
│   ├── api/v1/endpoints/  # Route logic
│   ├── core/              # Global config
│   ├── models/            # DB models
│   ├── schemas/           # Pydantic validation
│   └── main.py            # App entry point
├── tests/                 # Pytest suite
└── requirements.txt