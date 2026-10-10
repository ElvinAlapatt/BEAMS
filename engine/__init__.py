"""BEAMS core engine package.

Pipeline contract (do NOT break — backend/frontend depend on it):

    engine.pipeline.run_analysis(video_path, job_id) -> backend.schemas.AnalysisResult

Phase 2 owners:
- detection/  -> YOLO finetune on cleaned_data_part_1 (nike/adidas/puma)
- tracking/   -> ByteTrack/SORT
- saliency/   -> spectral-residual now, DeepGaze later
- scoring.py  -> already real formula, just tune weights in configs/scoring.yaml
"""
