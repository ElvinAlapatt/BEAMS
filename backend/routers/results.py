"""Fetch analysis results + CSV export."""
from __future__ import annotations

import csv
import io

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from backend import store
from backend.schemas import AnalysisResult

router = APIRouter(prefix="/api/results", tags=["results"])


@router.get("/{job_id}", response_model=AnalysisResult)
def get_result(job_id: str) -> AnalysisResult:
    if job_id not in store.results:
        raise HTTPException(404, "result not ready or unknown job_id")
    return AnalysisResult(**store.results[job_id])


@router.get("/{job_id}/csv")
def get_csv(job_id: str) -> StreamingResponse:
    if job_id not in store.results:
        raise HTTPException(404, "result not ready or unknown job_id")
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["brand", "exposures", "total_seconds",
                                        "avg_area_ratio", "avg_saliency", "attention_score"])
    w.writeheader()
    w.writerows(store.results[job_id]["brands"])
    buf.seek(0)
    return StreamingResponse(iter([buf.read()]), media_type="text/csv",
                             headers={"Content-Disposition": f"attachment; filename=beams_{job_id}.csv"})
