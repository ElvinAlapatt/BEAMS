"""Upload + run analysis (stub runs dummy engine synchronously).

Phase 2: make this async (BackgroundTasks / Celery) + real YOLO.
"""
from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend import store
from backend.schemas import JobStatus
from engine.pipeline import run_analysis

router = APIRouter(prefix="/api/jobs", tags=["jobs"])

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED = {".mp4", ".avi", ".mov", ".mkv", ".webm"}


@router.post("", response_model=JobStatus)
def create_job(file: UploadFile = File(...)) -> JobStatus:
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED:
        raise HTTPException(400, f"Unsupported format {suffix}. Use MP4/AVI/MOV/MKV/WebM.")
    job_id = store.new_job_id()
    dest = RAW_DIR / f"{job_id}_{Path(file.filename or 'upload.mp4').name}"
    dest.write_bytes(file.file.read())

    store.jobs[job_id] = {"job_id": job_id, "status": "processing",
                          "video_name": file.filename, "detail": "analyzing..."}
    try:
        result = run_analysis(str(dest), job_id=job_id)
        store.results[job_id] = result.model_dump()
        store.jobs[job_id].update(status="ready", detail="done")
    except Exception as exc:  # keep starter robust; surface error to UI
        store.jobs[job_id].update(status="failed", detail=str(exc))
    return JobStatus(**store.jobs[job_id])


@router.get("/{job_id}", response_model=JobStatus)
def get_job(job_id: str) -> JobStatus:
    if job_id not in store.jobs:
        raise HTTPException(404, "unknown job_id")
    return JobStatus(**store.jobs[job_id])
