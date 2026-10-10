"""BEAMS Streamlit UI — upload -> brand leaderboard -> Q&A -> export.

Run backend first:  uv run uvicorn backend.main:app --reload
Then:               streamlit run frontend/app.py
If backend is down, the app falls back to running engine.pipeline locally
so teammates can still demo without the API.
"""
from __future__ import annotations

import os
import tempfile

import requests
import streamlit as st

API = os.getenv("BEAMS_API", "http://127.0.0.1:8000")

st.set_page_config(page_title="BEAMS | Brand Exposure Analytics", page_icon="📺", layout="wide")
st.title("BEAMS — Brand Exposure Analytics")
st.caption("Attention-aware sponsorship measurement (starter: dummy detections, real scoring formula)")

# ---------- helpers ----------
def api_upload(video_bytes: bytes, name: str) -> dict | None:
    try:
        r = requests.post(f"{API}/api/jobs", files={"file": (name, video_bytes)}, timeout=120)
        r.raise_for_status()
        return r.json()
    except Exception as exc:
        st.warning(f"Backend unavailable ({exc}) — using local engine fallback.")
        return None


def api_result(job_id: str) -> dict | None:
    try:
        r = requests.get(f"{API}/api/results/{job_id}", timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def api_chat(job_id: str, question: str) -> str | None:
    try:
        r = requests.post(f"{API}/api/chat", json={"job_id": job_id, "question": question}, timeout=30)
        r.raise_for_status()
        return r.json()["answer"]
    except Exception:
        return None


def local_run(video_bytes: bytes, name: str) -> dict:
    from engine.pipeline import run_analysis
    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{name}") as f:
        f.write(video_bytes)
        tmp = f.name
    # minimal valid mp4 header check — engine.probe raises a clear error otherwise
    res = run_analysis(tmp, job_id="local")
    return res.model_dump()

# ---------- upload ----------
up = st.file_uploader("Upload match clip", type=["mp4", "mov", "avi", "mkv", "webm"])
if up is None:
    st.info("Upload a football highlight to get Nike / Adidas / Puma exposure + attention scores.")
    st.stop()

st.video(up)
if st.button("▶ Run BEAMS analysis", type="primary"):
    with st.spinner("Analyzing (downsample → detect → track → score)…"):
        job = api_upload(up.getvalue(), up.name)
        if job and job.get("status") in ("ready", "processing"):
            res = api_result(job["job_id"])
            st.session_state["result"] = res
            st.session_state["job_id"] = job["job_id"]
            st.session_state["via"] = "backend"
        else:
            res = local_run(up.getvalue(), up.name)
            st.session_state["result"] = res
            st.session_state["job_id"] = res["job_id"]
            st.session_state["via"] = "local-engine"
    st.rerun()

# ---------- results ----------
res = st.session_state.get("result")
if not res:
    st.stop()

st.success(f"Done via {st.session_state.get('via')} · {res['frames_analyzed']} frames @ {res['fps_sampled']}fps")
brands = res["brands"]

c1, c2, c3 = st.columns(3)
for col, b in zip((c1, c2, c3), brands[:3]):
    col.metric(f"{b['brand'].title()} — attention", f"{b['attention_score']}",
               f"{b['exposures']} exposures · {b['total_seconds']}s")

st.subheader("Brand leaderboard (by attention score)")
st.dataframe(brands, use_container_width=True)
st.bar_chart({b["brand"]: b["attention_score"] for b in brands})

# ---------- Q&A ----------
st.subheader("Ask about the results")
q = st.text_input("e.g. Which brand had the most attention?  /  Compare all brands  /  How did Nike do?")
if q:
    job_id = st.session_state.get("job_id", "local")
    ans = api_chat(job_id, q) if st.session_state.get("via") == "backend" else None
    if ans is None:  # local fallback mirrors backend rule-based logic
        from backend.routers.chat import answer_question
        ans = answer_question(brands, q)
    st.write(ans)

# ---------- export ----------
st.subheader("Export")
st.download_button("⬇ Download CSV", data=str(brands).encode(), file_name=f"beams_{res['job_id']}.csv")
st.caption(f"API CSV (when backend up): {API}/api/results/{res['job_id']}/csv")
