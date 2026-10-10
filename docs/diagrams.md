# Diagrams — use-case, DFDs, architecture, state

Two renderings of the same truth: **mermaid** in `architecture.md` (renders on
GitHub, always in sync by hand) and **PNGs** from `docs/diagrams_arch.py`
(`diagrams` library, for the PDF report). If they ever disagree, the `.py` is
authoritative — regenerate the PNGs and copy the structure into mermaid.

```bash
sudo apt install graphviz   # binary, once per machine (Windows: graphviz.org/download)
uv run python docs/diagrams_arch.py   # → docs/diagrams/{architecture,dfd_level0,dfd_level1}.png
```

## Use-case diagram

Actors (SRS §7): **Sponsor/Brand Manager**, **Marketing Analyst**,
**Event Organiser**, **Researcher**, (+ Developer).

```
  Sponsor/Analyst/Organiser ──► Upload Video ──► Run Analysis ──► View Brand Dashboard
        │                                                     ├──► Ask in English
        │                                                     └──► Export Report (CSV/PDF)
  Researcher ──► Evaluate Performance (mAP / precision / recall)
  Developer ──► Retrain Detector / Tune Scoring Weights
```

Include-relations: `Run Analysis` includes `Detect Logos`, `Track Logos`,
`Compute Visibility`, `Compute Saliency`, `Fuse Attention Score`.
`Ask in English` extends `View Brand Dashboard`.

## DFD Level-0 (context)

External entities: **User**, **Annotated Dataset**. Single process: BEAMS.

```
User ──video + question──► (BEAMS) ──dashboard + answers + reports──► User
Annotated Dataset ──train/eval labels──► (BEAMS)
```

## DFD Level-1 (subsystems)

```
1.0 Ingest & Downsample:  video ──► 2fps frames (+ metadata)
2.0 Detect & Track:       frames ──► tracks {track_id, brand, bbox, conf}
3.0 Attention Scoring:    tracks + saliency maps ──► per-brand scores
4.0 Report & Q&A:         scores + metrics ──► charts, NL answers, CSV/PDF
5.0 Evaluate:             predictions × ground truth ──► mAP / P / R
```

Data stores: `D1 raw clips`, `D2 downsampled frames`, `D3 annotations`,
`D4 tracks+scores`, `D5 weights`.

## DFD Level-2 (inside 2.0 + 3.0)

```
frame ──► YOLO ──► NMS ──► SORT/ByteTrack associate ──► smoothed track bboxes
   ├──► saliency model ──► saliency map ──► mean inside bbox ──► saliency_mean
track bbox + saliency_mean ──► visibility calc ──► × saliency ──► frame_score
frame_scores ──► temporal aggregate ──► BrandScore
```

## Architecture (layered + pipeline)

```
[Streamlit GUI] ──REST poll──► [FastAPI: jobs / results / chat + store]
                                     ──► [Engine: video_io → YOLO → ByteTrack → saliency → scoring]
                                     ──► [LangGraph agent (Phase 3)] ──► answers grounded in stored results
                                     ──► [Evaluation module]
[SQLite (Phase 2)] replaces in-memory store; [models/ + data/] persist artefacts.
```

Deployment: single desktop (SRS §5.1/§8: Windows/macOS/Linux, 8GB RAM,
GPU recommended for training only).

## State diagram (analysis job)

```
IDLE ──upload valid──► QUEUED ──worker picks──► PREPROCESSING ──► DETECTING
  ──► TRACKING ──► SCORING ──► READY ──► Q&A_ACTIVE ──► REPORT_EXPORTED ──► IDLE
any ──corrupt video / exception──► FAILED ──retry──► QUEUED
```

Per-track sub-states: `Tentative ──► Confirmed ──► Occluded ──► Lost/Closed`.
