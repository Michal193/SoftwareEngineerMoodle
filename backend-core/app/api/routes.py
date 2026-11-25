from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
from app.data.supabase_client import SupabaseNotConfigured
from app.services import infra_check

router = APIRouter()


class CheckIn(BaseModel):
    message: str
    author: str = "anonymous"


@router.get("/ping")
def ping():
    return {"domain": "core", "pong": True}


def _wrap(fn):
    try:
        return fn()
    except SupabaseNotConfigured as e:
        raise HTTPException(status_code=503, detail=str(e))
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"Supabase error: {e.response.text}")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Cannot reach Supabase: {e}")


@router.post("/infra-check")
def post_check(body: CheckIn):
    return _wrap(lambda: infra_check.create_check(body.message, body.author))


@router.get("/infra-check")
def get_checks():
    return _wrap(lambda: infra_check.latest_checks())
