from cdf.common.clocks import ClockModel, LocalClock
from cdf.common.config import load_run_config
import pytest


def test_affine_clock_and_shared_tick_timestamp():
    c = LocalClock(ClockModel(0.37, 1.002), seed=10)
    assert c.stamp(4.0, 100)[0] == pytest.approx(4.378)
    assert c.stamp(4.0, 100) == c.stamp(4.0, 100)
    assert c.stamp(5.0, 120)[1] - c.stamp(4.0, 100)[1] == 20
    assert c.stamp(4.0, 100)[1] != 100


def test_profile_and_jitter_are_reproducible_monotonic_and_independent():
    cfg = load_run_config().with_overrides(
        {
            "clocks": {
                "independent": True,
                "offset": {"enabled": True, "max_abs_s": 0.4},
                "drift": {"enabled": True, "max_abs_ppm": 100},
                "jitter": {"enabled": True, "std_s": 0.1},
            }
        }
    )
    a, again, b = [
        LocalClock.for_participant(cfg, 3, p, "S01/crash") for p in ["A", "A", "B"]
    ]
    x = [a.stamp(i * 0.05, i) for i in range(300)]
    assert x == [again.stamp(i * 0.05, i) for i in range(300)]
    assert all(x[i + 1][0] > x[i][0] for i in range(len(x) - 1))
    assert a.model != b.model
    assert abs(a.model.offset_s) <= 0.4
    assert abs(a.model.drift_ppm) <= 100
    assert a.ground_truth() == again.ground_truth()


def test_synchronized_baseline_and_invalid_models():
    c = LocalClock.for_participant(
        load_run_config().with_overrides({"clocks": {"independent": False}}), 0, "A"
    )
    assert c.stamp(5.0, 200) == (5.0, 200)
    with pytest.raises(ValueError):
        ClockModel(scale=0)
    with pytest.raises(ValueError):
        LocalClock(ClockModel(), jitter_std_s=-1)
