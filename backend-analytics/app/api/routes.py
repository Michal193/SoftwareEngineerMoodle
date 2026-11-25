from fastapi import APIRouter
from app.services import analytics_service

router = APIRouter()


@router.get("/ping")
def ping():
    return analytics_service.ping()
