from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session

# Syntax: Import schemas and models using aliases for cleaner code
from app.schemas import task as schemas
from app.models import task as models

# Syntax: Import the dependency that yields our database connection
from app.database import get_db

router = APIRouter()

@router.get("/", response_model=list[schemas.TaskResponse])
def get_all_tasks(
    db: Session = Depends(get_db),
    # Syntax: FastAPI automatically reads these from the URL query string
    skip: int = Query(0, ge=0, description="Number of tasks to skip"),
    limit: int = Query(100, le=100, description="Max tasks to return"),
    status: Optional[bool] = Query(None, description="Filter by 'done' status")
):
    # 1. Base Query: We don't use .all() yet, so this stays in Python memory
    # and doesn't hit the PostgreSQL database yet.
    query = db.query(models.Task)

    # 2. Filter Logic: If the user provided '?status=true' or '?status=false'
    if status is not None:
        query = query.filter(models.Task.done == status)

    # 3. Pagination Logic: Translates directly to SQL 'OFFSET' and 'LIMIT'
    # .all() physically executes the query against the database.
    tasks = query.offset(skip).limit(limit).all()

    return tasks

@router.post("/", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: schemas.TaskCreate, db: Session = Depends(get_db)):
    # Syntax: Unpack the Pydantic schema into the SQLAlchemy model
    # Logic: **task_data.model_dump() turns the JSON into keyword arguments (title="...", description="...")
    new_task = models.Task(**task_data.model_dump())

    # Logic: Put it in the workspace, save it to disk, and fetch the new ID
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_one_task(task_id: int, db: Session = Depends(get_db)):
    # Syntax: .filter(condition).first()
    # Logic: Translates to "SELECT * FROM tasks WHERE id = task_id LIMIT 1" in SQL.
    # We use .first() because IDs are unique; it stops searching after finding the match.
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    # Syntax: Fetch the specific task first
    # Logic: You cannot delete a record if you don't grab it from the warehouse first.
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # Syntax: db.delete(object)
    # Logic: Tell the session workspace to queue a DELETE command for this specific object.
    db.delete(task)

    # Syntax: db.commit()
    # Logic: Physically execute the DELETE command on the Postgres hard drive.
    db.commit()

    # Clean return statement!
    return {"message": "Deleted successfully"}
