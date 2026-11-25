from fastapi import APIRouter
from app.services import ai_service

router = APIRouter()


@router.get("/ping")
def ping():
    return ai_service.ping()
