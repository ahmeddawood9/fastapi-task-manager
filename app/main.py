from fastapi import FastAPI
from app.api.v1.endpoints import tasks, auth
from app.database import engine

# Import models so SQLAlchemy knows they exist before creating tables
from app.models import task as task_models
from app.models import user as user_models

# Syntax: Create Tables
# Logic: Because we imported both task and user models above, SQLAlchemy
# will physically build both the 'tasks' and 'users' tables in PostgreSQL.
task_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

# Syntax: Include the modular routers
# Logic: Connects your separate API files to the main application.
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/")
def root():
    # Syntax & Logic Fix: A clean dictionary with a properly closed string.
    return {"message": "Task Manager connected to PostgreSQL! View docs at /docs"}
