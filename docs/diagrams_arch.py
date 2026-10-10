"""Generate BEAMS architecture + DFD diagrams as code (diagrams lib).

Install:  uv sync            (pip package `diagrams`)
System:   sudo apt install graphviz   (or https://graphviz.org/download/)
Run:      uv run python docs/diagrams_arch.py
Output:   docs/diagrams/architecture.png, dfd_level0.png, dfd_level1.png

These PNGs are what you paste into the SRS/academic report.
Edit the `with Diagram(...)` blocks below to evolve them — no drag-and-drop tool.
"""
from __future__ import annotations

from pathlib import Path

OUT = Path(__file__).parent / "diagrams"
OUT.mkdir(exist_ok=True)

from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import Users
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.storage import NFS
from diagrams.programming.flowchart import Action, Decision, InputOutput

graph_attr = {"fontsize": "14", "bgcolor": "white", "pad": "0.5"}


def architecture() -> None:
    with Diagram("BEAMS Architecture (Streamlit + FastAPI, no websockets)",
                 filename=str(OUT / "architecture"), format="png",
                 show=False, graph_attr=graph_attr, direction="LR"):
        user = Users("Sponsor /\nAnalyst")
        with Cluster("Frontend"):
            ui = Action("Streamlit\nupload + dashboard\n+ Q&A")
        with Cluster("Backend (FastAPI REST polling)"):
            api = Server("jobs / results\n/ chat routers")
        with Cluster("Engine (Python/PyTorch/OpenCV)"):
            vio = InputOutput("video_io\n2fps downsample")
            det = Action("YOLO detect\n(nike/adidas/puma)")
            trk = Action("ByteTrack\ntracking")
            sal = Action("saliency\nmap")
            sco = Decision("scoring\nvisibility × saliency")
        store = NFS("data/ + models/")
        llm = Action("LangGraph\nreport agent\n(Phase 3)")
        user >> Edge(label="upload / poll") >> ui >> Edge(label="POST jobs") >> api
        api >> vio >> det >> trk >> sco
        sal >> Edge(label="saliency mean") >> sco
        sco >> store
        api >> store
        store >> llm >> api


def dfd0() -> None:
    with Diagram("BEAMS DFD Level-0 (Context)", filename=str(OUT / "dfd_level0"),
                 format="png", show=False, graph_attr=graph_attr, direction="LR"):
        user = Users("User")
        ext = NFS("Annotated\ndataset")
        sys = Action("BEAMS")
        user >> Edge(label="video + question") >> sys
        ext >> Edge(label="train/eval labels") >> sys
        sys >> Edge(label="dashboard + answers + reports") >> user


def dfd1() -> None:
    with Diagram("BEAMS DFD Level-1", filename=str(OUT / "dfd_level1"),
                 format="png", show=False, graph_attr=graph_attr, direction="LR"):
        vid = InputOutput("broadcast\nvideo")
        p1 = Action("1.0 ingest &\ndownsample")
        p2 = Action("2.0 detect\n& track")
        p3 = Action("3.0 attention\nscoring")
        p4 = Action("4.0 report\n& Q&A")
        p5 = Action("5.0 evaluate\nmAP/P/R")
        out = Users("dashboard /\nreport")
        vid >> p1 >> p2 >> p3 >> p4 >> out
        p2 >> p5


if __name__ == "__main__":
    architecture()
    dfd0()
    dfd1()
    print(f"wrote {[str(p) for p in sorted(OUT.glob('*.png'))] or 'PNGs need graphviz installed'}")
