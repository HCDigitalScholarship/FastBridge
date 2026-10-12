"""SM-2 scheduling for recall-mode flashcard review.

Pure arithmetic - no database, no clock. ``now`` is passed in rather than read
from ``datetime.utcnow()`` so the interval maths stays deterministic under test.
This function is the whole algorithm; everything around it is plumbing.
"""
from datetime import timedelta

RATINGS = ("again", "hard", "good", "easy")
MIN_EASE = 1.3
MAX_INTERVAL = 365


def schedule(state, rating, now):
    """Return the study_meta fields for ``rating`` applied to ``state``.

    ``state`` is None on a word's first review. Anki's flavour of SM-2: Again
    resets the repetition count and costs ease, Good graduates 1 -> 6 ->
    interval * ease, Easy takes the Good interval and adds a bonus.
    """
    s = state or {}
    ease = s.get("ease", 2.5)
    interval = s.get("interval", 0)
    reps = s.get("reps", 0)
    lapses = s.get("lapses", 0)

    if rating == "again":
        ease = max(MIN_EASE, ease - 0.20)
        interval, reps, lapses = 1, 0, lapses + 1
    else:
        if rating == "hard":
            ease = max(MIN_EASE, ease - 0.15)
            # +1 day floor, not just 1: round(1 * 1.2) is 1, so a card answered
            # Hard over and over would otherwise never leave a 1-day interval.
            interval = max(interval + 1, round(interval * 1.2))
        else:
            interval = 1 if reps == 0 else 6 if reps == 1 else round(interval * ease)
            if rating == "easy":
                interval = max(1, round(interval * 1.3))
                ease += 0.15
        reps += 1

    interval = min(interval, MAX_INTERVAL)
    # Due at the *start* of the target day, the way every SRS treats a day
    # boundary. An exact `now + interval` timestamp would mean a card reviewed
    # at 22:30 isn't available again until 22:30, so studying in the evening
    # would quietly push every card a day later. The day is in ``now``'s own
    # timezone, which the caller sets to the reviewer's.
    due = now + timedelta(days=interval)
    return {
        "interval": interval,
        "ease": round(ease, 4),
        "reps": reps,
        "lapses": lapses,
        "due": due.replace(hour=0, minute=0, second=0, microsecond=0),
        "last_review": now,
    }
