"""backend-core - Core & User Management.
Layers: api/ (HTTP routes) -> services/ (business logic) -> data/ (Supabase access).
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

SERVICE_NAME = os.getenv("SERVICE_NAME", "backend-core")

app = FastAPI(title="backend-core", description="Core & User Management")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router, prefix="/api/core")


@app.get("/health")
def health():
    return {"status": "ok", "service": SERVICE_NAME}
