"""Map cleaned_data_part_1 (classification folders, no boxes) -> YOLO dataset.

Current state (checked): nike 550 / adidas 433 / puma 37 / multi 164 /
needs_review 3694 / negatives 6700 — full-frame 1920x1080 jpgs, NO labels.

Step 1 (manual, once): upload `multi/` + a sample of each brand to Roboflow/CVAT,
  draw boxes, export YOLO (images + *.txt + data.yaml) into data/yolo_raw/.
Step 2 (this script): split into train/val, copy negatives as background images.

Run: uv run python research/prepare_dataset.py --src data/yolo_raw --dst data/yolo
"""
from __future__ import annotations

import argparse
import random
import shutil
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="data/yolo_raw")
    ap.add_argument("--dst", default="data/yolo")
    ap.add_argument("--val-frac", type=float, default=0.2)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    src = Path(args.src)
    dst = Path(args.dst)
    if not (src / "images").exists():
        print(f"No {src}/images yet — annotate in Roboflow first, then re-run.")
        print("Expected: data/yolo_raw/images/*.jpg + data/yolo_raw/labels/*.txt + data.yaml")
        return
    imgs = sorted((src / "images").glob("*.jpg"))
    rng = random.Random(args.seed)
    rng.shuffle(imgs)
    n_val = max(1, int(len(imgs) * args.val_frac))
    splits = {"val": imgs[:n_val], "train": imgs[n_val:]}
    for split, files in splits.items():
        for kind in ("images", "labels"):
            (dst / split / kind).mkdir(parents=True, exist_ok=True)
        for im in files:
            shutil.copy2(im, dst / split / "images" / im.name)
            lb = src / "labels" / (im.stem + ".txt")
            if lb.exists():  # negatives/backgrounds have NO label file — that is correct
                shutil.copy2(lb, dst / split / "labels" / lb.name)
    print(f"done: {len(splits['train'])} train / {len(splits['val'])} val -> {dst}")
    print("next: yolo detect train data=data/yolo/data.yaml model=yolov8m.pt epochs=50 imgsz=640")


if __name__ == "__main__":
    main()
