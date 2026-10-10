"""Detector metrics (pure numpy) — precision / recall / mAP@0.5.

Usage (Phase 2, after annotating cleaned_data_part_1):
    prec, rec = precision_recall(pred_boxes, gt_boxes, iou_thr=0.5)
"""
from __future__ import annotations


def iou(a: list[float], b: list[float]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1, ix2, iy2 = max(ax1, bx1), max(ay1, by1), min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0.0, ix2 - ix1), max(0.0, iy2 - iy1)
    inter = iw * ih
    union = (ax2 - ax1) * (ay2 - ay1) + (bx2 - bx1) * (by2 - by1) - inter
    return inter / union if union > 0 else 0.0


def precision_recall(pred: list[list[float]], gt: list[list[float]],
                     iou_thr: float = 0.5) -> tuple[float, float]:
    """Greedy 1-to-1 match. Returns (precision, recall)."""
    matched_gt: set[int] = set()
    tp = 0
    for p in pred:
        for i, g in enumerate(gt):
            if i not in matched_gt and iou(p, g) >= iou_thr:
                matched_gt.add(i)
                tp += 1
                break
    prec = tp / len(pred) if pred else 0.0
    rec = tp / len(gt) if gt else 0.0
    return round(prec, 4), round(rec, 4)
