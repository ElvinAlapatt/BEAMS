# Frontend — Streamlit UI

Run: `uv run streamlit run frontend/app.py` (backend first, or standalone —
the app works either way). Source: single file `frontend/app.py`.

## Screens (top to bottom)

1. **Upload** — file picker (MP4/MOV/AVI/MKV/WebM) with inline preview.
2. **Run** — `▶ Run BEAMS analysis` POSTs to `/api/jobs`, polls
   `/api/results/{id}`, stores the result in session state.
3. **Leaderboard** — top-3 attention metric cards, full brand table
   (`brand, exposures, total_seconds, avg_area_ratio, avg_saliency,
   attention_score`), bar chart of attention scores.
4. **Q&A** — text box; answers come from `/api/chat`, e.g.
   `Which brand had the most attention?`, `Compare all brands`, `How did Nike do?`
5. **Export** — CSV download (via `/api/results/{id}/csv` when the backend is up).

## Backend / local fallback

`BEAMS_API` env (default `http://127.0.0.1:8000`) points at the backend.
If the POST fails (backend down), the app imports `engine.pipeline` and runs
the analysis in-process, tagging results `via: local-engine` instead of `backend`.
Same schema, same screens — demos never die to a dead terminal.

## Phase 2+ UI work

- Frame scrubber with bbox overlays (serve annotated frames from
  `data/processed/`).
- Attention-over-time line chart per brand (needs per-frame series endpoint).
- Sponsorship-value estimate panel (SRS §13.3: score → currency model).
- Keep the page count low: one main page + `pages/` only when a screen earns it.
