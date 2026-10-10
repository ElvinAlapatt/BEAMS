# evaluation — detector + tracker + attention metrics (SRS §4.3)

- `metrics_det.py` — precision / recall / mAP@0.5 from YOLO pred vs GT boxes
- Phase 2 adds `metrics_track.py` (MOTA/IDF1) and human-gaze correlation.
- Run: `uv run pytest tests/ evaluation/` (pure-numpy, no GPU)
