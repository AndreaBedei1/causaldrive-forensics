"""How a run of contacts becomes a list of impacts.

CARLA reports a contact every tick it lasts, and again every half second once
two vehicles have come to rest against each other. Turning that into "how many
times did they collide" is the whole of `_pair_impacts`, and getting it wrong is
invisible: a chain of settling contacts reappears as a second impact seconds
later, and whichever check reads the second impact is then reading bodywork.
"""

from __future__ import annotations

from cdf.simulation.scenario_checks import _pair_impacts


def contact(t: float, a: str, b: str, impulse: float) -> dict:
    return {"t": t, "participant_id": a, "other_participant_id": b,
            "impulse": impulse, "is_participant_pair": True}


def test_a_pairs_first_contact_counts_however_light_it_was() -> None:
    """S13's 17.7 N.s corner clip: a collision, and one the run reported."""
    impacts = _pair_impacts([contact(5.1, "A", "B", 17.7)])
    assert [(i["pair"], i["impulse"]) for i in impacts] == [(("A", "B"), 17.7)]


def test_a_settling_chain_after_a_real_impact_is_not_a_second_one() -> None:
    rows = [contact(5.7, "A", "B", 26142.0)]
    rows += [contact(8.55 + 0.5 * i, "A", "B", 130.0) for i in range(6)]
    impacts = _pair_impacts(rows)
    assert [round(i["t"], 2) for i in impacts] == [5.7]


def test_the_same_pair_colliding_again_in_earnest_still_counts() -> None:
    """The floor is about gentleness, not about having touched before."""
    impacts = _pair_impacts([contact(5.7, "A", "B", 26142.0),
                             contact(9.0, "A", "B", 5000.0)])
    assert [round(i["t"], 2) for i in impacts] == [5.7, 9.0]


def test_contact_that_persists_is_one_impact_however_long_it_lasts() -> None:
    """Every tick for two seconds is one collision, not forty."""
    rows = [contact(5.3 + 0.05 * i, "A", "B", 3000.0 if i == 0 else 100.0)
            for i in range(40)]
    impacts = _pair_impacts(rows)
    assert len(impacts) == 1 and impacts[0]["impulse"] == 3000.0


def test_impacts_of_different_pairs_are_never_merged() -> None:
    impacts = _pair_impacts([contact(6.0, "B", "C", 9416.0),
                             contact(6.1, "A", "B", 11677.0)])
    assert [i["pair"] for i in impacts] == [("B", "C"), ("A", "B")]
