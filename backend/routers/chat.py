"""Rule-based Q&A stub (no LLM needed for starter).

Phase 3: replace `answer_question` with a LangGraph agent that reads
AnalysisResult + generates grounded summaries. Keep same endpoint.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend import store
from backend.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/chat", tags=["chat"])


def answer_question(brands: list[dict], question: str) -> str:
    q = question.lower()
    if not brands:
        return "No brands detected in this video."
    top = max(brands, key=lambda b: b["attention_score"])
    if "top" in q or "best" in q or "most" in q:
        return (f"{top['brand']} has the highest attention score "
                f"({top['attention_score']:.1f}) with {top['exposures']} exposures "
                f"over {top['total_seconds']:.1f}s.")
    for b in brands:
        if b["brand"].lower() in q:
            return (f"{b['brand']}: {b['exposures']} exposures, "
                    f"{b['total_seconds']:.1f}s total, attention score {b['attention_score']:.1f} "
                    f"(avg size {b['avg_area_ratio']:.3f}, saliency {b['avg_saliency']:.2f}).")
    if "compare" in q or "vs" in q or "all" in q:
        ranking = ", ".join(f"{b['brand']} ({b['attention_score']:.1f})"
                            for b in sorted(brands, key=lambda b: -b["attention_score"]))
        return f"Brand ranking by attention score: {ranking}."
    if "long" in q or "duration" in q or "exposure" in q:
        longest = max(brands, key=lambda b: b["total_seconds"])
        return (f"{longest['brand']} has the longest exposure "
                f"({longest['total_seconds']:.1f}s across {longest['exposures']} detections).")
    return (f"Analyzed {len(brands)} brand(s). Top is {top['brand']} "
            f"(score {top['attention_score']:.1f}). Ask e.g. 'Compare all brands' or 'How did Nike do?'.")


@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    if req.job_id not in store.results:
        raise HTTPException(404, "run analysis first (unknown job_id)")
    ans = answer_question(store.results[req.job_id]["brands"], req.question)
    return ChatResponse(job_id=req.job_id, question=req.question, answer=ans)
