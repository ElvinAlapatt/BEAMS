# BEAMS Architecture (starter)

`Streamlit --REST/poll--> FastAPI --> engine.pipeline --> data/models`
No websockets — polling is enough until live-broadcast phase.

```mermaid
flowchart LR
  U[User: Sponsor / Analyst] --> UI[Streamlit: upload + leaderboard + Q&A]
  UI -->|POST /api/jobs, GET results, POST chat| API[FastAPI: jobs/results/chat]
  API --> VIO[video_io: 2fps downsample]
  VIO --> DET[YOLO: nike/adidas/puma]
  DET --> TRK[ByteTrack]
  TRK --> SCO[scoring: visibility x saliency]
  SAL[saliency map] --> SCO
  SCO --> STORE[data/ + models/]
  STORE --> LLM[LangGraph report agent - Phase 3]
  LLM --> API
```

## DFD Level-0

```mermaid
flowchart LR
  U[User] -->|video + question| B[BEAMS]
  D[Annotated dataset] -->|train/eval labels| B
  B -->|dashboard + answers + reports| U
```

## DFD Level-1

```mermaid
flowchart LR
  V[Broadcast video] --> P1[1.0 ingest & downsample]
  P1 --> P2[2.0 detect & track]
  P2 --> P3[3.0 attention scoring]
  P3 --> P4[4.0 report & Q&A]
  P4 --> O[dashboard / report]
  P2 --> P5[5.0 evaluate: mAP/P/R]
```

## Job state diagram

```mermaid
stateDiagram-v2
  [*] --> queued: upload valid MP4/AVI
  queued --> processing: worker picks up
  processing --> ready: pipeline returns AnalysisResult
  processing --> failed: corrupt video / exception
  failed --> queued: retry upload
  ready --> [*]
```

> Pretty PNGs for the report: `uv run python docs/diagrams_arch.py` (needs graphviz).
