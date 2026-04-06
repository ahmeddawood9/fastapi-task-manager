from fastapi import APIRouter, HTTPException, status
from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.database import tasks_db, counter

router = APIRouter()

@router.get("/", response_model=list[Task])
def get_all_tasks():
    return tasks_db

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate):
    new_task = {
        "id": counter.next_id(),
        **task_data.model_dump()
    }
    tasks_db.append(new_task)
    return new_task

@router.get("/{task_id}", response_model=Task)
def get_one_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            tasks_db.pop(index)
            return {"message": "Deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")
