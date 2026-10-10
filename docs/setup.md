# Setup — install, run, verify

## Prerequisites

- Python 3.11+ (repo pins `>=3.11`; CI uses 3.12)
- [`uv`](https://docs.astral.sh/uv/) — `curl -LsSf astral.sh/uv/install.sh | sh`
- Git. Optional: Graphviz binary (only for `docs/diagrams_arch.py` PNGs),
  GPU + CUDA (only Phase 2 training; the starter runs on CPU).

> WSL note: the repo lives on a Windows mount (`/mnt/d/...`). `uv sync` copies
> instead of hardlinking there, so the first install takes a few minutes.
> That's normal — or move the clone under `~/` for speed.

## Install & verify

```bash
uv sync --group dev   # runtime + pytest/httpx
uv run pytest -q      # expect: all green (scoring maths + full API flow)
```

What the tests prove: `tests/test_scoring.py` checks the attention formula stays
in `[0,100]` and rewards centred, salient, large logos; `tests/test_api.py`
builds a synthetic mp4 with OpenCV, uploads it, fetches results + CSV logic, and
chats — no GPU, no weights, no network.

## Run the system

```bash
# terminal 1 — backend, interactive docs at http://127.0.0.1:8000/docs
uv run uvicorn backend.main:app --reload

# terminal 2 — frontend
uv run streamlit run frontend/app.py
```

Point the UI at a non-default backend: `cp .env.example .env`, edit `BEAMS_API`.

## Everyday commands

| Task | Command |
|---|---|
| Run API | `uv run uvicorn backend.main:app --reload` |
| Run UI | `uv run streamlit run frontend/app.py` |
| Tests | `uv run pytest -q` (single file: `uv run pytest tests/test_scoring.py -q`) |
| Downsample a clip manually | `uv run python -c "from engine.video_io import downsample; print(len(downsample('data/raw/clip.mp4')))"` |
| Local analysis (no API) | `uv run python -c "from engine.pipeline import run_analysis; print(run_analysis('data/raw/clip.mp4').model_dump())"` |
| Report PNGs | `uv run python docs/diagrams_arch.py` (needs Graphviz binary) |
| YOLO dataset split | `uv run python research/prepare_dataset.py --src data/yolo_raw --dst data/yolo` |

## Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `uv sync` hangs with no output | It's copying wheels across filesystems; check with `tail -f /tmp/beams_sync.log` (or just wait). Never `Ctrl-C` mid-sync — re-run it. |
| `ModuleNotFoundError: cv2` | Re-run `uv sync --group dev`; always execute via `uv run` so the project venv is used. |
| `uvicorn: command not found` | Same — use `uv run uvicorn ...`. |
| Streamlit shows "Backend unavailable" | Backend isn't up or `BEAMS_API` is wrong; UI falls back to local engine, results still appear (badge shows `local-engine`). |
| Upload rejected (400) | Extension not in MP4/AVI/MOV/MKV/WebM, or file is corrupt — check job `detail`. |
| `diagrams_arch.py` → `ExecutableNotFound: graphviz` | `pip install diagrams` isn't enough; install the binary: `sudo apt install graphviz` (Windows: graphviz.org/download, add to PATH). |
| GPU OOM in Phase 2 training | Reduce `imgsz` to 416, batch to 8, or train on downsampled frames; see `dataset.md`. |
