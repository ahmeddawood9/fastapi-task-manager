from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import task as task_models
from app.models import user as user_models
from app.schemas import task as task_schemas
from app.api.deps import get_current_user

router = APIRouter()

# --- CREATE ---
@router.post("/", response_model=task_schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task: task_schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user)
):
    # Force the new task to be owned by the user holding the JWT token
    new_task = task_models.Task(**task.model_dump(), owner_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# --- READ ALL ---
@router.get("/", response_model=List[task_schemas.Task])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user)
):
    # The Bouncer guarantees current_user exists. Now we only fetch THEIR tasks.
    tasks = db.query(task_models.Task).filter(task_models.Task.owner_id == current_user.id).offset(skip).limit(limit).all()
    return tasks

# --- READ ONE ---
@router.get("/{task_id}", response_model=task_schemas.Task)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user)
):
    # Query must match both the task ID AND the owner's ID
    task = db.query(task_models.Task).filter(
        task_models.Task.id == task_id,
        task_models.Task.owner_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found or not authorized")
    return task

# --- UPDATE ---
@router.put("/{task_id}", response_model=task_schemas.Task)
def update_task(
    task_id: int,
    task_update: task_schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user)
):
    task_query = db.query(task_models.Task).filter(
        task_models.Task.id == task_id,
        task_models.Task.owner_id == current_user.id
    )
    task = task_query.first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found or not authorized")

    task_query.update(task_update.model_dump(), synchronize_session=False)
    db.commit()
    return task_query.first()

# --- DELETE ---
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user)
):
    task_query = db.query(task_models.Task).filter(
        task_models.Task.id == task_id,
        task_models.Task.owner_id == current_user.id
    )
    task = task_query.first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found or not authorized")

    task_query.delete(synchronize_session=False)
    db.commit()
    # 204 No Content shouldn't return anything
    return None
