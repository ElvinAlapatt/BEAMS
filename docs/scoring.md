# Attention-aware visibility score — the research contribution

SRS §1.1/§1.3: exposure alone ≠ impact. A pitch-side LED board dead-centre in
frame is worth more than a blurred sleeve logo at the edge, even with identical
screen time. BEAMS multiplies **what was visible** by **whether anyone looked**.

## Per-frame attention (one logo detection)

All inputs normalised to `[0,1]`; output scaled to `[0,100]` for readability.
Implementation: `engine/scoring.frame_attention`, weights from `configs/scoring.yaml`.

```
centre_prox  = 1 - dist((xc,yc), (0.5,0.5)) / 0.7071     # 1 at centre → 0 at corner
visibility   = w_area·area_ratio + w_center·centre_prox + w_sharp·sharpness
attention    = visibility · (α + (1-α)·saliency_mean)
frame_score  = attention · 100
```

- `area_ratio` — bbox area / frame area (size on screen).
- `centre_prox` — broadcast bias: directors frame the action centrally, so centre
  ≈ fovea. Computed in `center_proximity()`.
- `sharpness` — Laplacian variance normalised (proxy for motion blur/focus;
  Phase 2 may add an occlusion penalty term).
- `saliency_mean` — mean of the saliency map inside the bbox ÷ frame mean.
  Today's stub synthesises it; Phase 2 computes it from the actual saliency model.
- `α` (default 0.3) — floor so a zero-saliency detection still keeps 30% of its
  visibility value instead of vanishing.

Defaults: `w_area=0.5, w_center=0.3, w_sharp=0.2, α=0.3`.

## Per-brand aggregation

```python
aggregate_brand(frame_scores, dt, video_duration)
total_seconds   = exposures × dt                 # dt = 1/target_fps
attention_score = Σ(frame_score × dt) / video_duration
```

Dividing by video duration makes scores comparable across clips of different
lengths. Brands sort descending by `attention_score` for the leaderboard.

## Worked example

Logo at centre (`centre_prox≈1`), `area=0.03`, `sharp=0.8`, `saliency=0.9`:

```
visibility = .5·.03 + .3·1 + .2·.8 = .015 + .3 + .16 = .475
attention  = .475 · (.3 + .7·.9) = .475 · .93 ≈ .442 → 44.2
```

Same logo at the corner (`centre_prox≈0.2`), blurry, unsalient
(`sharp=0.3, saliency=0.2`):

```
visibility = .015 + .06 + .06 = .135
attention  = .135 · (.3 + .14) ≈ .059 → 5.9
```

~7.5× difference for identical screen time — that gap is the thesis.

## Tuning & validation

- Tune `configs/scoring.yaml`, never the formula, so ablations are diffable.
- Invariants pinned by `tests/test_scoring.py`: bounded output, centre beats
  corner, saliency/size monotonicity, duration normalisation.
- Phase 3 validation: correlate `attention_score` against human gaze fixations
  (if eye-tracking data is collected) and against sponsor recall surveys.
