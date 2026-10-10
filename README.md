# BEAMS — Brand Exposure Analytics and Metrics System

Sports sponsorship is one of the most valuable forms of brand marketing, yet its
effectiveness is hard to measure. Existing tools count **how long** a logo is on
screen and treat every appearance as equally valuable. BEAMS measures **how much
attention** each appearance actually earns: it detects sponsor logos in sports
broadcast footage, tracks them across frames, weights each exposure by visual
saliency (where viewers are likely to look), and answers questions about the
results in plain English.

> Academic spec: `research/academics/srs.pdf`. Start there, then
> `docs/` for every subsystem.

## What it does (SRS scope)

1. **Detect + track** sponsor logos (`nike`, `adidas`, `puma`) in match footage
   — YOLO detector + ByteTrack/SORT tracker.
2. **Score attention** — classic visibility metrics (duration, coverage, size,
   position) fused with a saliency estimate into one attention-aware score.
3. **Report in English** — dashboard, brand leaderboard, Q&A chat, CSV/PDF export.
4. **Evaluate** — mAP / precision / recall for detection, MOTA/IDF1 for tracking.

## Quickstart (clone → running in ~5 min, no GPU needed)

```bash
git clone https://github.com/ElvinAlapatt/BEAMS.git && cd BEAMS
uv sync --group dev        # creates .venv, installs deps
uv run pytest -q           # must be green before you push

# terminal 1 — API (docs at http://127.0.0.1:8000/docs)
uv run uvicorn backend.main:app --reload

# terminal 2 — UI
uv run streamlit run frontend/app.py
```

Upload a match clip → brand leaderboard → ask
`"Compare all brands"` → download CSV. If the backend isn't running, the UI
automatically falls back to the local engine so demos still work.

Set the API URL (default `http://127.0.0.1:8000`) via env:

```bash
cp .env.example .env   # then edit BEAMS_API if needed
```

## How it works (30-second version)

```
match clip (60fps)
  → downsample to 2fps            (engine/video_io.py — 30x cheaper, same signal)
  → YOLO detects logos per frame  (engine/pipeline.py — dummy now, real model Phase 2)
  → ByteTrack links them          (same interface, swapped in later)
  → saliency map per frame        (spectral-residual now, TranSalNet later)
  → attention = visibility × saliency, aggregated per brand
  → FastAPI serves JSON           (backend/routers/)
  → Streamlit shows leaderboard + chat answers from the numbers
```

The scoring formula is already real (`engine/scoring.py`, weights in
`configs/scoring.yaml`) — only the detector/tracker/saliency backends are stubs.

## Repo map

| Path | What lives here | Doc |
|---|---|---|
| `backend/` | FastAPI app: `jobs` (upload), `results` (JSON/CSV), `chat` (Q&A). REST polling, **no websockets** | `docs/api.md` |
| `engine/` | `pipeline.py` contract `run_analysis(video) → AnalysisResult`; `scoring.py` attention formula; `video_io.py` downsampling | `docs/pipeline.md`, `docs/scoring.md` |
| `frontend/` | Streamlit: upload → leaderboard → Q&A → export | `docs/frontend.md` |
| `configs/` | `inference.yaml` (fps, thresholds), `scoring.yaml` (attention weights) | `docs/pipeline.md` |
| `data/` | `raw/ → downsampled/ → annotations/ → processed/ → metrics/` (gitignored, see README inside) | `docs/dataset.md` |
| `models/` | `yolo/beams.pt`, `saliency/` checkpoints (gitignored) | `docs/dataset.md` |
| `evaluation/` | precision / recall / mAP (`metrics_det.py`), tracking + gaze later | `docs/evaluation.md` |
| `research/` | SRS, notebooks, `prepare_dataset.py` (external frames → YOLO splits) | `docs/dataset.md` |
| `docs/` | Architecture, DFDs, setup, roadmap; `diagrams_arch.py` generates report PNGs | `docs/README.md` |
| `tests/` | `test_scoring.py`, `test_api.py` — run on every change | `docs/setup.md` |

## Current data (outside the repo, not committed)

`cleaned_data_part_1/cleaned/`: `nike 550`, `adidas 433`, `puma 37`,
`multi 164`, `needs_review 3694`, `negatives 6700` — full-frame 1920×1080
stills from football highlights, **no bounding boxes yet**. They become YOLO
training data only after annotation (Roboflow/CVAT → `research/prepare_dataset.py`).
Details + class-imbalance plan in `docs/dataset.md`.

## Diagrams for the report

Mermaid sources render on GitHub in `docs/architecture.md`. Pretty PNGs via the
`diagrams` library (needs the Graphviz binary once per machine):

```bash
sudo apt install graphviz   # Windows: https://graphviz.org/download/
uv run python docs/diagrams_arch.py   # → docs/diagrams/*.png
```

Use-case, DFD Level-0/1/2, architecture and state diagrams are all described in
`docs/diagrams.md`.

## Team workflow

- `main` is always green (`pytest` + CI). Branch per owner: `feat/detection`,
  `feat/tracking`, `feat/saliency`, `feat/chat`, `feat/eval`.
- The seam between teams is `engine/pipeline.py::run_analysis` — don't break its
  signature; everything else is swappable. Task board + phases in `docs/roadmap.md`.
- New here? Read in order: this file → `docs/setup.md` → `docs/architecture.md`
  → your subsystem doc from the table above.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `uv sync` slow on `/mnt/d` (WSL) | Normal — Windows-mount copies are slow; wait it out, or move repo under `~/` |
| `cv2` import error | `uv sync --group dev` reinstalls `opencv-python`; needs no system libs for the wheel |
| Streamlit can't reach API | Check `BEAMS_API` in `.env`, backend running on `:8000`, try `/health` |
| `diagrams_arch.py` fails | Install Graphviz binary (see above) — the pip package alone isn't enough |
| Video rejected on upload | Only MP4/AVI/MOV/MKV/WebM; corrupt files return `status: failed` with reason |

## License / contributing

Academic project (Group A03). PRs welcome — open an issue first for major changes,
keep `pytest -q` green, never commit videos, weights, or secrets.
