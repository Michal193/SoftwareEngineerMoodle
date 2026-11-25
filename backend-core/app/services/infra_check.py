"""Business layer for the infrastructure check (Frontend -> Backend -> Supabase)."""
from app.data import supabase_client as db

TABLE = "infra_checks"


def create_check(message: str, author: str) -> dict:
    rows = db.insert(TABLE, {"message": message, "author": author})
    return rows[0] if rows else {}


def latest_checks(limit: int = 10) -> list:
    return db.select(TABLE, f"select=*&order=created_at.desc&limit={limit}")
