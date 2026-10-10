# Roadmap — phases, owners, definition of done

## Phase 0 — Starter (done, this repo)

Cloneable skeleton: API + engine contract + UI + tests + docs + diagrams-as-code.
Exit: `uv sync && uv run pytest -q` green on every teammate's machine.

## Phase 1 — Data (owner: data)

Triage `cleaned_data_part_1`, annotate in Roboflow, `research/prepare_dataset.py`
→ `data/yolo/` splits. Exit: 80/20 split, `data.yaml`, Puma rescued from
`needs_review/`, dedupe verified. (Detail: `dataset.md`.)

## Phase 2 — Perception (owners: detection / tracking / saliency)

- **Detection:** finetune `yolov8m` → `models/yolo/beams.pt`, `mAP@0.5 ≥ 0.70`.
- **Tracking:** ByteTrack wrapper in `engine/tracking/`, MOTA/IDF1 reported.
- **Saliency:** spectral-residual baseline in `engine/saliency/`, DeepGaze later.
- Wire all three into `run_analysis`, keep its signature. Exit: real `AnalysisResult`
  on a held-out clip + `evaluation/` numbers. (Detail: `pipeline.md`.)

## Phase 3 — Language + value (owners: chat / eval)

LangGraph agent over stored results (grounded, cites numbers), PDF export,
sponsorship-valuation mapping (SRS §13.3), gaze-correlation study.
Exit: demo-day story — upload → leaderboard → "Why did Adidas win?" → PDF.

## Task board (suggested branches)

| Task | Branch | Done when |
|---|---|---|
| Annotate + split dataset | `feat/dataset` | `data/yolo/{train,val}` + `data.yaml` |
| Train YOLO baseline | `feat/detection` | `beams.pt` + mAP logged |
| ByteTrack integration | `feat/tracking` | stable IDs, MOTA/IDF1 logged |
| Saliency backend | `feat/saliency` | real `saliency_mean` in pipeline |
| LangGraph chat | `feat/chat` | answers cite stored numbers |
| Eval expansion | `feat/eval` | per-brand P/R, robustness slices |
| Report figures | `feat/report` | PNGs regenerated, SRS updated |

Rules: `main` stays green (CI runs `pytest`), one PR per task, never commit
videos / weights / secrets.
