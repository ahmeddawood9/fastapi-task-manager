from pydantic import BaseModel, ConfigDict
from typing import Optional

# Syntax: Base Schema
# Logic: Shared properties for creating and reading tasks.
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    done: bool = False

# Syntax: Create Schema
# Logic: What the user is required to send in the POST request body.
class TaskCreate(TaskBase):
    pass

# Syntax: Response Schema
# Logic: What FastAPI will return to the user (includes the DB-generated ID).
class Task(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
