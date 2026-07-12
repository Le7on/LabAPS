"""Unit tests for the shift calendar mapping (ADR-016)."""

from __future__ import annotations

import pytest

from backend.engines.planning.calendar import (
    build_calendar,
    map_interval,
    slot_count,
)


def test_single_mode_hourly_slots_per_day():
    # One unit = one hour; single shift 09:00-17:00 = 8 hourly slots/day.
    slots = build_calendar("2026-08-10", "2026-08-12", "single")
    assert len(slots) == 24  # 3 days x 8 hours
    assert slots[0].shift_code == "Shift1"
    assert slots[0].start_at.isoformat() == "2026-08-10T09:00:00"
    assert slots[0].end_at.isoformat() == "2026-08-10T10:00:00"
    assert slots[7].end_at.isoformat() == "2026-08-10T17:00:00"
    assert slots[8].day.isoformat() == "2026-08-11"


def test_double_mode_hourly_slots_per_day():
    slots = build_calendar("2026-08-10", "2026-08-11", "double")
    # 2 days x 16 hours (two 8h shifts).
    assert len(slots) == 32
    assert slots[0].start_at.isoformat() == "2026-08-10T06:00:00"
    assert slots[0].shift_code == "Shift1"
    # Hour 8 begins the second shift at 14:00.
    assert slots[8].start_at.isoformat() == "2026-08-10T14:00:00"
    assert slots[8].shift_code == "Shift2"
    assert slots[15].end_at.isoformat() == "2026-08-10T22:00:00"
    assert slots[16].day.isoformat() == "2026-08-11"


def test_skipped_dates_produce_no_slots():
    slots = build_calendar("2026-08-10", "2026-08-12", "single", ["2026-08-11"])
    assert {s.day.isoformat() for s in slots} == {"2026-08-10", "2026-08-12"}
    # Indices stay contiguous across the skipped day (16 hours over 2 days).
    assert [s.index for s in slots] == list(range(16))


def test_slot_count():
    assert slot_count("2026-08-10", "2026-08-14", "single") == 5 * 8
    assert slot_count("2026-08-10", "2026-08-14", "double") == 5 * 16
    assert slot_count("2026-08-10", "2026-08-14", "single", ["2026-08-11", "2026-08-12"]) == 3 * 8


def test_map_interval_within_calendar():
    slots = build_calendar("2026-08-10", "2026-08-12", "single")
    # First two hours of day one.
    mapped = map_interval(slots, 0, 2)
    assert mapped["startAt"] == "2026-08-10T09:00:00"
    assert mapped["endAt"] == "2026-08-10T11:00:00"
    assert mapped["shift"] == "Shift1"


def test_map_interval_out_of_range_or_empty():
    slots = build_calendar("2026-08-10", "2026-08-10", "single")  # 8 hourly slots
    assert map_interval(slots, 0, 0) is None  # empty
    assert map_interval(slots, 0, 99) is None  # beyond capacity


def test_unknown_mode_and_bad_range():
    with pytest.raises(ValueError):
        build_calendar("2026-08-10", "2026-08-12", "triple")
    with pytest.raises(ValueError):
        build_calendar("2026-08-12", "2026-08-10", "single")
