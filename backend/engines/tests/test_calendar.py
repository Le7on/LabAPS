"""Unit tests for the shift calendar mapping (ADR-016)."""

from __future__ import annotations

import pytest

from backend.engines.planning.calendar import (
    build_calendar,
    map_interval,
    slot_count,
)


def test_single_mode_one_slot_per_day():
    slots = build_calendar("2026-08-10", "2026-08-12", "single")
    assert [s.index for s in slots] == [0, 1, 2]
    assert slots[0].shift_code == "Shift1"
    assert slots[0].start_at.isoformat() == "2026-08-10T09:00:00"
    assert slots[0].end_at.isoformat() == "2026-08-10T17:00:00"
    assert slots[1].day.isoformat() == "2026-08-11"


def test_double_mode_two_slots_per_day():
    slots = build_calendar("2026-08-10", "2026-08-11", "double")
    # 2 days x 2 shifts = 4 slots.
    assert [s.shift_code for s in slots] == ["Shift1", "Shift2", "Shift1", "Shift2"]
    assert slots[0].start_at.isoformat() == "2026-08-10T06:00:00"
    assert slots[1].start_at.isoformat() == "2026-08-10T14:00:00"
    assert slots[1].end_at.isoformat() == "2026-08-10T22:00:00"
    # Second day starts a new date.
    assert slots[2].day.isoformat() == "2026-08-11"


def test_skipped_dates_produce_no_slots():
    slots = build_calendar("2026-08-10", "2026-08-12", "single", ["2026-08-11"])
    assert [s.day.isoformat() for s in slots] == ["2026-08-10", "2026-08-12"]
    # Indices stay contiguous across the skipped day.
    assert [s.index for s in slots] == [0, 1]


def test_slot_count():
    assert slot_count("2026-08-10", "2026-08-14", "single") == 5
    assert slot_count("2026-08-10", "2026-08-14", "double") == 10
    assert slot_count("2026-08-10", "2026-08-14", "single", ["2026-08-11", "2026-08-12"]) == 3


def test_map_interval_within_calendar():
    slots = build_calendar("2026-08-10", "2026-08-12", "single")
    mapped = map_interval(slots, 0, 2)
    assert mapped["startAt"] == "2026-08-10T09:00:00"
    assert mapped["endAt"] == "2026-08-11T17:00:00"
    assert mapped["shift"] == "Shift1"


def test_map_interval_out_of_range_or_empty():
    slots = build_calendar("2026-08-10", "2026-08-10", "single")
    assert map_interval(slots, 0, 0) is None  # empty
    assert map_interval(slots, 0, 5) is None  # beyond capacity


def test_unknown_mode_and_bad_range():
    with pytest.raises(ValueError):
        build_calendar("2026-08-10", "2026-08-12", "triple")
    with pytest.raises(ValueError):
        build_calendar("2026-08-12", "2026-08-10", "single")
