from fastapi import FastAPI
from app.api.v1.api import api_router

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.ratelimit import limiter

# Import models so SQLAlchemy knows they exist before creating tables
from app.models import task as task_models
from app.models import user as user_models



app = FastAPI(title="Task Manager API")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Syntax: Include the modular routers
# Logic: Connects your separate API files to the main application.
app.include_router(api_router)

@app.get("/")
def root():
    # Syntax & Logic Fix: A clean dictionary with a properly closed string.
    return {"message": "Task Manager connected to PostgreSQL! View docs at /docs"}
