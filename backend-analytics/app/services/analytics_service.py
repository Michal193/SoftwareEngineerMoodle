from typing import Optional
from app.data import supabase_client
from app.models.task import Task, TaskCreate, TaskStatus


def ping() -> dict:
    return {"domain": "analytics", "pong": True}


def create_task(payload: TaskCreate) -> Task:
    row = payload.model_dump(mode="json")
    inserted = supabase_client.insert("tasks", row)
    return Task(**inserted[0])


def list_tasks(
    student_id: Optional[str] = None,
    course_id: Optional[str] = None,
    status: Optional[TaskStatus] = None,
    open_only: bool = False,
) -> list[Task]:
    filters = ["select=*"]
    if student_id:
        filters.append(f"student_id=eq.{student_id}")
    if course_id:
        filters.append(f"course_id=eq.{course_id}")
    if status:
        filters.append(f"status=eq.{status}")
    elif open_only:
        filters.append("status=neq.completed")
    query = "&".join(filters)
    rows = supabase_client.select("tasks", query=query)
    return [Task(**r) for r in rows]


def complete_task(task_id: int) -> Optional[Task]:
    updated = supabase_client.update(
        "tasks",
        query=f"id=eq.{task_id}",
        data={"status": "completed"},
    )
    if not updated:
        return None
    return Task(**updated[0])


def delete_task(task_id: int) -> bool:
    deleted = supabase_client.delete("tasks", query=f"id=eq.{task_id}")
    return bool(deleted)