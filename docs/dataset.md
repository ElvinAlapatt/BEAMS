# Dataset — from match frames to YOLO weights

## In-repo layout (`data/`, gitignored except `README.md`)

```
data/raw/          original 60fps clips (never commit)
data/downsampled/  1–2fps jpgs (regenerable via engine.video_io.downsample)
data/annotations/  YOLO labels: data.yaml + *.txt (commit ONLY data.yaml + tiny sample)
data/processed/    tracks + per-frame scores (parquet/json, regenerable)
data/metrics/      aggregated leaderboards (csv)
models/yolo/beams.pt, models/saliency/*  (weights — never commit)
```

## External source: `cleaned_data_part_1` (as audited)

`cleaned/`: `nike 550`, `adidas 433`, `puma 37`, `multi 164`,
`needs_review 3694`, `negatives 6700` — 1920×1080 full frames, **no boxes**.

- **Usable now:** brand-diverse, real broadcast domain, `negatives/` are free
  background images (YOLO: image with no label file = negative).
- **Must fix before training:** (1) no bounding boxes — folder names are not
  labels, YOLO needs `*.txt` boxes; (2) `puma:37` is ~12× rarer than Nike —
  mine `needs_review/` for Puma, add augmentation + class weights;
  (3) triage `needs_review/` (blurry/unusable → drop, multi-logo → keep, they
  train multi-box images); (4) near-duplicate consecutive frames — dedupe by
  perceptual hash or temporal stride so val isn't contaminated.
- Stays **outside** the repo (11k images). Only the export + `data.yaml` pattern
  is documented here.

## Annotation → training path

1. Upload `multi/` + brand samples to **Roboflow** (recommended, free academic)
   or CVAT. Classes: `nike, adidas, puma`. Box every visible logo ≥ ~15px.
2. Export **YOLOv8** format into `data/yolo_raw/` (`images/`, `labels/`, `data.yaml`).
3. Split: `uv run python research/prepare_dataset.py --src data/yolo_raw --dst data/yolo`
   (stratified 80/20, negatives copied as background images).
4. Train (GPU machine): `yolo detect train data=data/yolo/data.yaml model=yolov8m.pt epochs=50 imgsz=640`
5. Export best to `models/yolo/beams.pt`, record mAP in `evaluation/`, wire into
   `engine/pipeline.py` replacing `_dummy_detections()`.

Target for sign-off: `mAP@0.5 ≥ 0.70` on the held-out split, precision/recall
reported per brand (Puma will lag — report it honestly, that's valid research).
