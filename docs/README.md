# docs — BEAMS documentation index

Read in this order:

1. `setup.md` — install, run, verify, troubleshoot (start here as a new teammate)
2. `architecture.md` — system overview: components, DFDs, state diagram (mermaid)
3. `pipeline.md` — engine: downsampling → detection → tracking → aggregation
4. `scoring.md` — the attention-aware visibility score (the research contribution)
5. `api.md` — FastAPI backend: endpoints, schemas, polling flow
6. `frontend.md` — Streamlit UI: screens, backend/local fallback, asking questions
7. `dataset.md` — data layout, `cleaned_data_part_1`, annotation → YOLO training
8. `evaluation.md` — precision/recall/mAP, tracking metrics, gaze correlation
9. `diagrams.md` — use-case, DFD Level-0/1/2, architecture, state diagrams for the report
10. `roadmap.md` — phases, team task board, definition of done

Report figures: `uv run python docs/diagrams_arch.py` → `docs/diagrams/*.png`
(requires the Graphviz binary; see `setup.md`). Mermaid versions of the same
diagrams live in `architecture.md` and render directly on GitHub.
