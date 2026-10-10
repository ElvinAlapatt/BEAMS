"""Pydantic schemas — single source of truth for API <-> frontend <-> engine."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class BrandScore(BaseModel):
    brand: str
    exposures: int = Field(ge=0)
    total_seconds: float = Field(ge=0)
    avg_area_ratio: float = Field(ge=0, le=1)
    avg_saliency: float = Field(ge=0, le=1)
    attention_score: float = Field(ge=0)


class AnalysisResult(BaseModel):
    job_id: str
    video_name: str
    fps_sampled: float
    frames_analyzed: int
    brands: list[BrandScore]


class JobStatus(BaseModel):
    job_id: str
    status: Literal["queued", "processing", "ready", "failed"]
    video_name: str
    detail: str = ""


class ChatRequest(BaseModel):
    job_id: str
    question: str


class ChatResponse(BaseModel):
    job_id: str
    question: str
    answer: str
