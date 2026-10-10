"""BEAMS FastAPI entrypoint. Run: uv run uvicorn backend.main:app --reload"""
from __future__ import annotations

from fastapi import FastAPI

from backend.routers import chat, jobs, results

app = FastAPI(title="BEAMS API", version="0.1.0",
              description="Brand Exposure Analytics and Metrics System (starter)")
app.include_router(jobs.router)
app.include_router(results.router)
app.include_router(chat.router)


@app.get("/", tags=["health"])
def root() -> dict:
    return {"status": "ok", "service": "BEAMS", "docs": "/docs"}


@app.get("/health", tags=["health"])
def health() -> dict:
    return {"ok": True}
