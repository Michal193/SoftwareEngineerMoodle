from typing import Optional
from fastapi import APIRouter, HTTPException
from app.data.supabase_client import SupabaseNotConfigured
from app.models.task import Task, TaskCreate
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
def list_tasks(student_id: Optional[str] = None, course_id: Optional[str] = None):
    try:
        return analytics_service.list_tasks(student_id=student_id, course_id=course_id)
    except SupabaseNotConfigured as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc