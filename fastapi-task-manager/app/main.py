from fastapi import FastAPI
from app.api.v1.endpoints import tasks
from app.database import engine
from app.models import task as models

# Syntax: Create Tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

# Syntax: Include the modular router
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])

@app.get("/")
def root():
    # Syntax & Logic Fix: A clean dictionary with a properly closed string.
    return {"message": "Task Manager connected to PostgreSQL! View docs at /docs"}
