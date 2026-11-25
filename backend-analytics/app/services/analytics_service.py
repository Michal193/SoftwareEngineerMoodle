"""Business layer for Analytics & Notifications. Add this team's logic here."""
from typing import Optional
from app.data import supabase_client
from app.models.task import Task, TaskCreate

def ping() -> dict:
    return {"domain": "analytics", "pong": True}

def create_task(payload: TaskCreate) -> Task:
    row = payload.model_dump(mode="json")
    inserted = supabase_client.insert("tasks", row)
    return Task(**inserted[0])


def list_tasks(student_id: Optional[str] = None, course_id: Optional[str] = None) -> list[Task]:
    filters = ["select=*"]
    if student_id:
        filters.append(f"student_id=eq.{student_id}")
    if course_id:
        filters.append(f"course_id=eq.{course_id}")
    query = "&".join(filters)
    rows = supabase_client.select("tasks", query=query)
    return [Task(**item) for item in rows]
