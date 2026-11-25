"""Data layer: thin wrapper over the Supabase REST API (PostgREST).
Keys come only from environment variables (.env) - never hard-code them."""
import os
import httpx


class SupabaseNotConfigured(Exception):
    pass


def _config():
    url, key = os.getenv("SUPABASE_URL", ""), os.getenv("SUPABASE_KEY", "")
    if not url or not key or "your_" in url or "your_" in key:
        raise SupabaseNotConfigured("SUPABASE_URL / SUPABASE_KEY are missing in .env")
    return url.rstrip("/"), key


def _headers(key):
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def insert(table: str, row: dict) -> list:
    url, key = _config()
    r = httpx.post(f"{url}/rest/v1/{table}", json=row, headers=_headers(key), timeout=10)
    r.raise_for_status()
    return r.json()


def select(table: str, query: str = "select=*") -> list:
    url, key = _config()
    r = httpx.get(f"{url}/rest/v1/{table}?{query}", headers=_headers(key), timeout=10)
    r.raise_for_status()
    return r.json()


def update(table: str, query: str, data: dict) -> list:
    url, key = _config()
    r = httpx.patch(f"{url}/rest/v1/{table}?{query}", json=data, headers=_headers(key), timeout=10)
    r.raise_for_status()
    return r.json()


def delete(table: str, query: str) -> list:
    url, key = _config()
    r = httpx.delete(f"{url}/rest/v1/{table}?{query}", headers=_headers(key), timeout=10)
    r.raise_for_status()
    return r.json()