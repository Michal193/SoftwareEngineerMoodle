from fastapi import APIRouter
from app.services import courses_service

router = APIRouter()


@router.get("/ping")
def ping():
    return courses_service.ping()
