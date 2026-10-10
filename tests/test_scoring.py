"""Scoring maths must stay in [0,100] and reward centre + saliency."""
from engine.scoring import aggregate_brand, center_proximity, frame_attention


def test_centre_beats_corner():
    assert center_proximity(0.5, 0.5) > center_proximity(0.05, 0.05) > 0


def test_attention_rewards_saliency_and_size():
    small = frame_attention(0.01, 0.5, 0.5, 0.8, 0.4)
    big = frame_attention(0.06, 0.5, 0.5, 0.8, 0.9)
    assert 0 <= small <= 100 and 0 <= big <= 100
    assert big > small


def test_aggregate_normalises_by_duration():
    agg = aggregate_brand([50.0, 60.0], dt=0.5, video_duration=10.0)
    assert agg["exposures"] == 2 and agg["total_seconds"] == 1.0
    assert agg["attention_score"] == round((110.0 * 0.5) / 10.0, 2)
