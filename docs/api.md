# Backend API — FastAPI, REST polling (no websockets)

Run: `uv run uvicorn backend.main:app --reload` → interactive docs at `/docs`.
Source: `backend/main.py`, `backend/routers/{jobs,results,chat}.py`,
`backend/schemas.py`, `backend/store.py`.

## Why polling, not websockets

Jobs finish in seconds on sampled frames, clients are few (teammates, demo
judges), and Streamlit polling is two lines of `requests`. Websockets would add
connection state, reconnect logic and deployment friction for zero MVP benefit.
Revisit only for SRS §13.3 live-broadcast analysis. The endpoint shapes already
support that migration (job status is a first-class resource).

## Endpoints

| Method | Path | Input | Output |
|---|---|---|---|
| `GET` | `/`, `/health` | — | liveness probes |
| `POST` | `/api/jobs` | multipart `file` (MP4/AVI/MOV/MKV/WebM) | `JobStatus` |
| `GET` | `/api/jobs/{job_id}` | — | `JobStatus` (poll this) |
| `GET` | `/api/results/{job_id}` | — | `AnalysisResult` |
| `GET` | `/api/results/{job_id}/csv` | — | leaderboard CSV download |
| `POST` | `/api/chat` | `{job_id, question}` | `{job_id, question, answer}` |

Errors: `400` unknown/unsupported upload format, `404` unknown `job_id` or result
not ready, `500` never raised intentionally — pipeline exceptions are captured
into job `status: failed` with the reason in `detail`.

## Flow

```
POST /api/jobs (file) ──→ save data/raw/{job}_{name} ──→ status=processing
   ──→ engine.pipeline.run_analysis() ──→ store result ──→ status=ready|failed
UI polls GET /api/jobs/{id}, then GET /api/results/{id}, renders leaderboard.
POST /api/chat answers from the stored numbers (rule-based now, LangGraph Phase 3).
```

## Schemas (`backend/schemas.py` — single source of truth)

- `BrandScore{brand, exposures, total_seconds, avg_area_ratio, avg_saliency, attention_score}`
- `AnalysisResult{job_id, video_name, fps_sampled, frames_analyzed, brands[]}`
- `JobStatus{job_id, status: queued|processing|ready|failed, video_name, detail}`
- `ChatRequest{job_id, question}` / `ChatResponse{job_id, question, answer}`

## Store & scaling

`backend/store.py` is an in-memory dict (`jobs`, `results`) — fine for a demo,
lost on restart. Phase 2 swaps it for SQLite (or Redis + `BackgroundTasks` for
true async) without touching routers: keep the function names, change the backend.
Upload cap / auth / rate-limiting are deliberately out of scope for the starter.
