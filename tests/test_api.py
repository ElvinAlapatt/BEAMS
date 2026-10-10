"""API smoke tests — no video/GPU needed (dummy engine + synthetic mp4)."""
import cv2
import numpy as np
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def _tiny_mp4(path: str, frames: int = 6) -> None:
    w = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"mp4v"), 30, (160, 120))
    for i in range(frames):
        w.write(np.full((120, 160, 3), i * 30 % 255, np.uint8))
    w.release()


def test_health():
    assert client.get("/health").json() == {"ok": True}


def test_full_flow_upload_results_chat(tmp_path):
    vid = str(tmp_path / "clip.mp4")
    _tiny_mp4(vid)
    with open(vid, "rb") as f:
        r = client.post("/api/jobs", files={"file": ("clip.mp4", f, "video/mp4")})
    assert r.status_code == 200, r.text
    job_id = r.json()["job_id"]

    res = client.get(f"/api/results/{job_id}")
    assert res.status_code == 200
    assert len(res.json()["brands"]) == 3  # nike / adidas / puma

    chat = client.post("/api/chat", json={"job_id": job_id, "question": "Compare all brands"})
    assert chat.status_code == 200 and "ranking" in chat.json()["answer"].lower()


def test_rejects_bad_format():
    r = client.post("/api/jobs", files={"file": ("x.txt", b"hi", "text/plain")})
    assert r.status_code == 400
