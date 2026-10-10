"""Attention-aware visibility scoring (REAL formula, no model needed).

Per-frame attention for one logo detection (SRS §1.3, §9):

    visibility  = w_area * area_ratio
                + w_center * center_proximity
                + w_sharp * sharpness            (all in [0,1])
    attention   = visibility * (alpha + (1 - alpha) * saliency_mean)
    frame_score = attention * 100                 (human-friendly scale)

Brand score = sum(frame_score * dt) / video_duration  -> comparable across videos.

Weights live in configs/scoring.yaml so researchers can tune without code changes.
"""
from __future__ import annotations


def center_proximity(xc: float, yc: float) -> float:
    """1.0 at frame centre, 0.0 at corner. xc, yc in [0,1]."""
    dx, dy = xc - 0.5, yc - 0.5
    dist = (dx * dx + dy * dy) ** 0.5          # 0 .. ~0.707
    return max(0.0, 1.0 - dist / 0.7071)


def frame_attention(area_ratio: float, xc: float, yc: float,
                    sharpness: float, saliency_mean: float,
                    w_area: float = 0.5, w_center: float = 0.3,
                    w_sharp: float = 0.2, alpha: float = 0.3) -> float:
    """Return frame attention in [0, 100]. All inputs in [0,1]."""
    area_ratio = min(max(area_ratio, 0.0), 1.0)
    sharpness = min(max(sharpness, 0.0), 1.0)
    saliency_mean = min(max(saliency_mean, 0.0), 1.0)
    visibility = (w_area * area_ratio
                  + w_center * center_proximity(xc, yc)
                  + w_sharp * sharpness)
    attention = visibility * (alpha + (1.0 - alpha) * saliency_mean)
    return round(attention * 100.0, 2)


def aggregate_brand(frame_scores: list[float], dt: float, video_duration: float) -> dict:
    """Aggregate per-frame scores of ONE track/brand to a summary."""
    if not frame_scores or video_duration <= 0:
        return {"exposures": 0, "total_seconds": 0.0, "attention_score": 0.0}
    total = sum(frame_scores) * dt
    return {
        "exposures": len(frame_scores),
        "total_seconds": round(len(frame_scores) * dt, 2),
        "attention_score": round(total / video_duration, 2),
    }
