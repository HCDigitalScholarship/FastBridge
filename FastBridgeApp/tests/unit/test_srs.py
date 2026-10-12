"""Unit tests for the SM-2 scheduler (utils/srs.py).

`schedule()` is pure and takes `now` as an argument, so every interval here is
checked against a fixed clock with no patching and no database. This is the
whole algorithm, so it gets the bulk of the coverage.
"""
from datetime import datetime, timedelta

import pytest

from utils import srs

NOW = datetime(2026, 1, 1, 12, 0, 0)


def _run(ratings, state=None):
    """Apply ratings in order, returning the final state."""
    for g in ratings:
        state = srs.schedule(state, g, NOW)
    return state


@pytest.mark.parametrize("rating,interval,reps,lapses", [
    ("again", 1, 0, 1),
    ("hard", 1, 1, 0),
    ("good", 1, 1, 0),
    # Easy multiplies the Good interval, and round(1 * 1.3) is still 1 - a new
    # card cannot skip its first day no matter which button you press.
    ("easy", 1, 1, 0),
])
def test_first_review_of_each_rating(rating, interval, reps, lapses):
    s = srs.schedule(None, rating, NOW)
    assert (s["interval"], s["reps"], s["lapses"]) == (interval, reps, lapses)
    assert s["due"] == (NOW + timedelta(days=interval)).replace(hour=0)
    assert s["last_review"] == NOW


def test_good_graduates_one_then_six_then_interval_times_ease():
    assert _run(["good"])["interval"] == 1
    assert _run(["good", "good"])["interval"] == 6
    # 6 * 2.5 = 15, then 15 * 2.5 = 38 (round-half-even on 37.5).
    assert _run(["good"] * 3)["interval"] == 15
    assert _run(["good"] * 4)["interval"] == 38


def test_easy_beats_good_once_there_is_an_interval_to_multiply():
    assert _run(["good", "easy"])["interval"] == 8      # round(6 * 1.3)
    assert _run(["good", "easy"])["ease"] == 2.65


def test_again_resets_reps_and_counts_a_lapse():
    s = _run(["good", "good", "good", "again"])
    assert s["interval"] == 1
    assert s["reps"] == 0
    assert s["lapses"] == 1
    # reps is back to 0, so the next Good starts the graduation over.
    assert srs.schedule(s, "good", NOW)["interval"] == 1


def test_ease_floors_at_1_3_under_repeated_again():
    s = _run(["again"] * 20)
    assert s["ease"] == srs.MIN_EASE
    assert s["lapses"] == 20


def test_hard_lowers_ease_and_grows_the_interval_slowly():
    s = _run(["good", "good"])                 # interval 6, ease 2.5
    h = srs.schedule(s, "hard", NOW)
    assert h["interval"] == 7                  # round(6 * 1.2)
    assert h["ease"] == 2.35
    assert h["reps"] == 3


def test_repeated_hard_still_grows_out_of_a_one_day_interval():
    """round(1 * 1.2) is 1, so a plain multiplier would pin a struggling card
    to a 1-day interval forever."""
    intervals = []
    s = None
    for _ in range(5):
        s = srs.schedule(s, "hard", NOW)
        intervals.append(s["interval"])
    assert intervals == [1, 2, 3, 4, 5]


def test_due_lands_on_a_day_boundary_not_the_review_time():
    """A card reviewed late at night has to be available the next morning."""
    evening = datetime(2026, 1, 1, 22, 30, 0)
    s = srs.schedule(None, "good", evening)
    assert s["interval"] == 1
    assert s["due"] == datetime(2026, 1, 2, 0, 0, 0)
    assert s["last_review"] == evening          # the exact time is still kept


def test_interval_caps_at_365_days():
    s = _run(["good"] * 12)
    assert s["interval"] == srs.MAX_INTERVAL
    assert s["due"] == (NOW + timedelta(days=365)).replace(hour=0)
    # The cap holds on Easy too, which multiplies on top of the Good interval.
    assert srs.schedule(s, "easy", NOW)["interval"] == srs.MAX_INTERVAL


def test_existing_state_is_not_mutated():
    state = {"interval": 6, "ease": 2.5, "reps": 2, "lapses": 0}
    srs.schedule(state, "good", NOW)
    assert state == {"interval": 6, "ease": 2.5, "reps": 2, "lapses": 0}
