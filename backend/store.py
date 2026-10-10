"""Shared in-memory job store (starter).

Phase 2 can swap this for SQLite / Redis without changing routers:
- jobs[job_id] -> JobStatus dict
- results[job_id] -> AnalysisResult dict
"""
from __future__ import annotations

import uuid

jobs: dict[str, dict] = {}
results: dict[str, dict] = {}


def new_job_id() -> str:
    return uuid.uuid4().hex[:8]
