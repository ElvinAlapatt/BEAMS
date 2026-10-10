# Evaluation — proving the numbers (SRS §4.3)

## Detection (implemented: `evaluation/metrics_det.py`)

Pure-numpy, no GPU: `iou()`, `precision_recall(pred, gt, iou_thr=0.5)` with
greedy 1-to-1 matching. `mAP@0.5` = mean AP over the 3 brand classes
(compute AP per class by sweeping confidence, then average).

Report per brand + overall: `mAP@0.5`, `mAP@0.5:0.95`, precision, recall, plus
robustness slices SRS §11 demands — motion blur, lighting change, occlusion
(tag val images, report the drop vs clean).

## Tracking (Phase 2: `evaluation/metrics_track.py`)

`MOTA` (misses + false positives + ID switches) and `IDF1` (identity
preservation) on annotated clip sequences. ID switches matter directly: a Nike
board that flips IDs mid-clip splits one exposure into two and corrupts duration.

## Attention score (Phase 3)

- **Sanity:** invariants in `tests/test_scoring.py` (bounded, centre > corner,
  saliency-monotone, duration-normalised).
- **Validity:** correlate brand `attention_score` with (a) human gaze fixations
  on the same clips if eye-tracking is available, (b) sponsor recall surveys.
  A score that predicts recalled brands better than raw screen time is the
  publishable result.

## Running it

```bash
uv run pytest -q                  # scoring invariants + API smoke (always green)
uv run pytest tests/ evaluation/  # + detector metrics once val labels exist
```

Every trained checkpoint gets a one-line entry (date, data hash, hyperparams,
mAP, per-brand P/R) — keep it in `evaluation/README.md` or a `RESULTS.md`
so ablations are comparable months later.
