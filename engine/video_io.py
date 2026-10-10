"""Video helpers: probe metadata + downsample raw 60fps -> 1-2fps frames.

Keeps the `data/raw -> data/downsampled` convention from data/README.md.
Real detection later runs on downsampled frames (30x cheaper, same sponsorship signal).
"""
from __future__ import annotations

from pathlib import Path

import cv2


def probe(video_path: str) -> dict:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    cap.release()
    return {"fps": fps, "frames": frames,
            "duration": round(frames / fps, 2) if fps else 0.0,
            "width": w, "height": h}


def downsample(video_path: str, out_dir: str = "data/downsampled",
               target_fps: float = 2.0) -> list[str]:
    """Extract frames at target_fps. Returns list of saved jpg paths."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video: {video_path}")
    src_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    step = max(1, int(round(src_fps / target_fps)))
    stem = Path(video_path).stem
    saved: list[str] = []
    idx, kept = 0, 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if idx % step == 0:
            p = out / f"{stem}_f{idx:06d}.jpg"
            cv2.imwrite(str(p), frame)
            saved.append(str(p))
            kept += 1
        idx += 1
    cap.release()
    return saved
