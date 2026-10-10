"""Starter pipeline — deterministic dummy that honours the real interface.

`run_analysis` is what backend calls. Today it:
  1. probes the video (real OpenCV),
  2. synthesises plausible detections for nike/adidas/puma (seeded by filename),
  3. scores them with engine.scoring (real formula),
  4. returns AnalysisResult (real schema).

Phase 2: replace _dummy_detections() with YOLO + tracker + saliency.
Nobody else's code changes — backend, frontend, tests keep working.
"""
from __future__ import annotations

import hashlib
import random
from pathlib import Path

import yaml

from backend.schemas import AnalysisResult, BrandScore
from engine import video_io
from engine.scoring import aggregate_brand, frame_attention

BRANDS = ["nike", "adidas", "puma"]


def _load_weights() -> dict:
    cfg = Path("configs/scoring.yaml")
    if cfg.exists():
        return yaml.safe_load(cfg.read_text()) or {}
    return {}


def _dummy_detections(video_path: str, n_frames: int) -> dict[str, list[dict]]:
    """Seeded pseudo-detections so same video -> same demo numbers."""
    seed = int(hashlib.md5(Path(video_path).name.encode()).hexdigest()[:8], 16)
    rng = random.Random(seed)
    out: dict[str, list[dict]] = {}
    for brand in BRANDS:
        n = rng.randint(max(1, n_frames // 8), max(2, n_frames // 3))
        dets = []
        for _ in range(n):
            dets.append({
                "area_ratio": round(rng.uniform(0.005, 0.06), 4),
                "xc": round(rng.uniform(0.3, 0.7), 3),
                "yc": round(rng.uniform(0.3, 0.7), 3),
                "sharpness": round(rng.uniform(0.4, 0.95), 3),
                "saliency": round(rng.uniform(0.3, 0.95), 3),
            })
        out[brand] = dets
    return out


def run_analysis(video_path: str, job_id: str = "local",
                 target_fps: float = 2.0) -> AnalysisResult:
    meta = video_io.probe(video_path)
    duration = meta["duration"] or 10.0
    n_frames = max(4, min(60, int(duration * target_fps)))
    dt = 1.0 / target_fps
    weights = _load_weights()

    detections = _dummy_detections(video_path, n_frames)
    brands: list[BrandScore] = []
    for brand, dets in detections.items():
        scores = [frame_attention(d["area_ratio"], d["xc"], d["yc"],
                                  d["sharpness"], d["saliency"],
                                  w_area=weights.get("w_area", 0.5),
                                  w_center=weights.get("w_center", 0.3),
                                  w_sharp=weights.get("w_sharp", 0.2),
                                  alpha=weights.get("alpha", 0.3))
                  for d in dets]
        agg = aggregate_brand(scores, dt, duration)
        area = round(sum(d["area_ratio"] for d in dets) / len(dets), 4)
        sal = round(sum(d["saliency"] for d in dets) / len(dets), 3)
        brands.append(BrandScore(brand=brand, exposures=agg["exposures"],
                                 total_seconds=agg["total_seconds"],
                                 avg_area_ratio=area, avg_saliency=sal,
                                 attention_score=agg["attention_score"]))
    brands.sort(key=lambda b: b.attention_score, reverse=True)
    return AnalysisResult(job_id=job_id, video_name=Path(video_path).name,
                          fps_sampled=target_fps, frames_analyzed=n_frames,
                          brands=brands)
