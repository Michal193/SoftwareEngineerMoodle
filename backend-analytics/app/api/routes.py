from typing import Optional
from fastapi import APIRouter, HTTPException
from app.data.supabase_client import SupabaseNotConfigured
from app.models.task import Task, TaskCreate, TaskStatus
from app.services import analytics_service

router = APIRouter()


@router.get("/ping")
def ping():
    return analytics_service.ping()


@router.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate):
    try:
        return analytics_service.create_task(payload)
    except SupabaseNotConfigured as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/tasks", response_model=list[Task])
def list_tasks(
    student_id: Optional[str] = None,
    course_id: Optional[str] = None,
    status: Optional[TaskStatus] = None,
    open_only: bool = False,
):
    try:
        return analytics_service.list_tasks(
            student_id=student_id,
            course_id=course_id,
            status=status,
            open_only=open_only,
        )
    except SupabaseNotConfigured as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: int):
    try:
        task = analytics_service.complete_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except HTTPException:
        raise
    except SupabaseNotConfigured as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    try:
        deleted = analytics_service.delete_task(task_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Task not found")
    except HTTPException:
        raise
    except SupabaseNotConfigured as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc