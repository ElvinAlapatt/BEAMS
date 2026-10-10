# data — NEVER commit videos. Gitignored except this README.

```
data/
  raw/          original 60fps match clips (MP4/AVI) — from highlights
  downsampled/  1-2fps jpgs via engine.video_io.downsample()
  annotations/  YOLO labels (Roboflow/CVAT export: *.txt + data.yaml)
  processed/    tracks + per-frame scores (parquet/json)
  metrics/      aggregated brand leaderboard (csv)
```

External set `cleaned_data_part_1/cleaned/` (nike 550 / adidas 433 / puma 37 /
multi 164 / needs_review 3694 / negatives 6700, no boxes yet) stays OUTSIDE
the repo. Convert it with `research/prepare_dataset.py` after annotating.
