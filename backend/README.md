# backend — FastAPI (REST polling, no websockets)

```
POST /api/jobs            upload clip  -> {job_id, status}
GET  /api/jobs/{id}       poll status
GET  /api/results/{id}    brand leaderboard JSON
GET  /api/results/{id}/csv
POST /api/chat            {job_id, question} -> grounded answer (rule-based now, LangGraph later)
```

Run: `uv run uvicorn backend.main:app --reload` → docs at `/docs`
