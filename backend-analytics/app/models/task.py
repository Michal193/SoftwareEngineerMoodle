from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel

TaskStatus = Literal["pending", "in_progress", "completed"]


class TaskCreate(BaseModel):
    student_id: str
    course_id: str
    title: str
    due_date: Optional[datetime] = None
    status: TaskStatus = "pending"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None


class Task(TaskCreate):
    id: int
    created_at: datetime