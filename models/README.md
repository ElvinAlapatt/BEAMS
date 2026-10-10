# models — weights are gitignored (*.pt/*.onnx). Commit this README only.

```
models/
  yolo/beams.pt      <- finetune output (Phase 2, from cleaned_data_part_1)
  saliency/          <- TranSalNet / DeepGaze checkpoint (Phase 3)
```

Starter needs NO weights (dummy pipeline). Get a baseline without training:
`yolov8m.pt` auto-downloads via ultralytics when Phase 2 starts.
