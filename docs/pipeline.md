# Engine pipeline — video in, brand scores out

File: `engine/pipeline.py`. Contract (backend, frontend and tests depend on it):

```python
run_analysis(video_path: str, job_id: str = "local", target_fps: float = 2.0) -> AnalysisResult
```

Stages today (★ = stub to be replaced in Phase 2, interface unchanged):

1. **Probe** — `engine/video_io.probe()` reads fps, frame count, duration via OpenCV.
   Corrupt/unreadable files raise `ValueError`, which the API surfaces as job `failed`.
2. **Downsample ★** — `engine/video_io.downsample()` keeps every Nth frame to hit
   `configs/inference.yaml: target_fps` (default 2.0). A 90-min match at 60fps is
   ~324k frames; at 2fps it's ~10.8k — the sponsorship signal is identical.
3. **Detect + track ★** — currently `_dummy_detections()`: seeded RNG per filename,
   so the same video always yields the same demo numbers. Phase 2 drops in YOLO
   (`models/yolo/beams.pt`) + ByteTrack here and returns the same
   `{area_ratio, xc, yc, sharpness, saliency}` dicts per detection.
4. **Score (REAL)** — every detection goes through `engine/scoring.frame_attention`
   with weights from `configs/scoring.yaml`; per-brand frames aggregate via
   `aggregate_brand` into `{exposures, total_seconds, attention_score}`.
5. **Return** — `backend.schemas.AnalysisResult` (brands sorted by attention),
   persisted by the API job store, rendered by Streamlit.

## Configs

- `configs/inference.yaml` — `target_fps`, `detector`, `conf_threshold`,
  `iou_threshold`, `tracker`. Phase 2 reads these instead of hardcoding.
- `configs/scoring.yaml` — `w_area / w_center / w_sharp / alpha`. Researchers tune
  the score without touching code; tests pin the formula's invariants.

## Ownership (parallel work)

- `detection/` (new package, owner A): finetune `yolov8m` on the annotated
  `cleaned_data_part_1` → export `models/yolo/beams.pt`, expose `detect(frames)`.
- `tracking/` (owner B): ByteTrack/SORT wrapper, expose `track(detections)`
  returning stable `track_id`s; evaluate MOTA/IDF1.
- `saliency/` (owner C): start with OpenCV spectral-residual
  (`cv2.saliency.StaticSaliencySpectralResidual`), later TranSalNet/DeepGaze;
  expose `saliency_mean(frame, bbox) -> float in [0,1]`.
- `scoring.py` is done — owners only adjust `scoring.yaml` + add ablation tests.
