"""Shift calendar mapping (ADR-016).

Maps the scheduler's integer time units to real calendar dates and shift time
windows. One integer unit = one shift slot. Slots are laid out day by day from a
start date to an end date, skipping any explicitly skipped dates. The shift mode
fixes each day's slots:

- single: one slot 09:00-17:00
- double: two slots 06:00-14:00 and 14:00-22:00

This is a pure module: no framework, no persistence, no OR-Tools.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta

SINGLE = "single"
DOUBLE = "double"

# Fixed shift windows per mode: (shift_code, start "HH:MM", end "HH:MM").
_SHIFT_WINDOWS: dict[str, tuple[tuple[str, str, str], ...]] = {
    SINGLE: (("Shift1", "09:00", "17:00"),),
    DOUBLE: (("Shift1", "06:00", "14:00"), ("Shift2", "14:00", "22:00")),
}


@dataclass(frozen=True, slots=True)
class Slot:
    """One shift slot on the calendar; ``index`` is its scheduler time unit."""

    index: int
    day: date
    shift_code: str
    start_at: datetime
    end_at: datetime


def _parse_date(value: str) -> date:
    return date.fromisoformat(value)


def _combine(day: date, hhmm: str) -> datetime:
    hour, minute = (int(p) for p in hhmm.split(":"))
    return datetime(day.year, day.month, day.day, hour, minute)


def build_calendar(
    start_date: str,
    end_date: str,
    shift_mode: str,
    skipped_dates: list[str] | None = None,
) -> list[Slot]:
    """Build the ordered list of shift slots for a plan's calendar.

    Days run inclusively from ``start_date`` to ``end_date``. Dates in
    ``skipped_dates`` produce no slots. Each remaining day contributes the slots
    of ``shift_mode`` in order. Slot ``index`` is the scheduler time unit.
    """
    windows = _SHIFT_WINDOWS.get(shift_mode)
    if windows is None:
        raise ValueError(f"Unknown shift mode: {shift_mode}")

    start = _parse_date(start_date)
    end = _parse_date(end_date)
    if end < start:
        raise ValueError("end_date must be on or after start_date")

    skip = {_parse_date(d) for d in (skipped_dates or [])}

    slots: list[Slot] = []
    day = start
    index = 0
    while day <= end:
        if day not in skip:
            for shift_code, start_hhmm, end_hhmm in windows:
                slots.append(
                    Slot(
                        index=index,
                        day=day,
                        shift_code=shift_code,
                        start_at=_combine(day, start_hhmm),
                        end_at=_combine(day, end_hhmm),
                    )
                )
                index += 1
        day += timedelta(days=1)
    return slots


def slot_count(
    start_date: str,
    end_date: str,
    shift_mode: str,
    skipped_dates: list[str] | None = None,
) -> int:
    """Total number of shift slots the calendar provides (the scheduler horizon)."""
    return len(build_calendar(start_date, end_date, shift_mode, skipped_dates))


def _expand_ranges(ranges: list | None) -> set[date]:
    """Expand [["YYYY-MM-DD","YYYY-MM-DD"], ...] inclusive ranges into a date set."""
    out: set[date] = set()
    for r in ranges or []:
        start = _parse_date(r[0])
        end = _parse_date(r[1])
        day = start
        while day <= end:
            out.add(day)
            day += timedelta(days=1)
    return out


def available_windows(
    slots: list[Slot], unavailable_ranges: list | None
) -> tuple[tuple[int, int], ...]:
    """Contiguous available [start_unit, end_unit) slot windows.

    Given the plan's slots and a resource's unavailable date ranges (leave,
    breakdown), return the maximal runs of consecutive slot indices whose day is
    NOT unavailable. A task fitting entirely within one such window therefore
    never touches an unavailable day. Empty ranges -> one window spanning all
    slots (fully available). No slots -> no windows.
    """
    if not slots:
        return ()
    blocked = _expand_ranges(unavailable_ranges)
    if not blocked:
        return ((0, len(slots)),)

    windows: list[tuple[int, int]] = []
    run_start: int | None = None
    for slot in slots:
        free = slot.day not in blocked
        if free and run_start is None:
            run_start = slot.index
        elif not free and run_start is not None:
            windows.append((run_start, slot.index))
            run_start = None
    if run_start is not None:
        windows.append((run_start, slots[-1].index + 1))
    return tuple(windows)


def day_window(slots: list[Slot], day: str) -> tuple[int, int] | None:
    """The [start, end) slot-index window covering a single calendar day.

    Returns None if the day has no slots (outside the calendar or skipped).
    """
    target = _parse_date(day)
    indices = [s.index for s in slots if s.day == target]
    if not indices:
        return None
    return (min(indices), max(indices) + 1)


def map_interval(slots: list[Slot], start_unit: int, end_unit: int) -> dict | None:
    """Map an integer [start_unit, end_unit) interval to real datetimes.

    Returns a dict with ``startAt`` (ISO datetime of the first slot's start),
    ``endAt`` (ISO datetime of the last occupied slot's end) and ``shift`` (the
    first slot's shift code). Returns None if the interval falls outside the
    calendar (e.g. an empty [t, t) or units beyond the available slots).
    """
    if end_unit <= start_unit:
        return None
    if start_unit < 0 or end_unit > len(slots):
        return None
    first = slots[start_unit]
    last = slots[end_unit - 1]
    return {
        "startAt": first.start_at.isoformat(),
        "endAt": last.end_at.isoformat(),
        "shift": first.shift_code,
    }
