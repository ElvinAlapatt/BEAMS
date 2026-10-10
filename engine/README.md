# engine — replace `_dummy_detections()` in pipeline.py with real stages:

- `detection/` (owner A): finetune `yolov8m` on `cleaned_data_part_1` → `models/yolo/beams.pt`
- `tracking/` (owner B): ByteTrack/SORT across downsampled frames
- `saliency/` (owner C): spectral-residual now → TranSalNet later
- `scoring.py` DONE (real formula) — tune `configs/scoring.yaml`
