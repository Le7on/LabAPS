"""Shift calendar mapping (ADR-016 / ADR-025).

Maps the scheduler's integer time units to real calendar dates and clock times.
One integer unit = one HOUR (durations/WorkHours are in hours). Hourly slots are
laid out within each day's shift windows, day by day from a start date to an end
date, skipping any explicitly skipped dates. The shift mode fixes each day's
working hours:

- single: 09:00-17:00 (8 hourly slots)
- double: 06:00-14:00 and 14:00-22:00 (16 hourly slots)

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
    """One hour on the calendar; ``index`` is its scheduler time unit (hours)."""

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
    include_weekends: bool = False,
    extra_workdays: list[str] | None = None,
) -> list[Slot]:
    """Build the ordered list of shift slots for a plan's calendar.

    Days run inclusively from ``start_date`` to ``end_date``. Weekends (Sat/Sun)
    are non-working by default and produce no slots unless ``include_weekends``
    is set. Dates in ``skipped_dates`` (holidays) also produce no slots. Dates in
    ``extra_workdays`` (overtime) DO get slots even if weekend/holiday — so at
    least one resource can work them (ADR-022). Each remaining day contributes
    the slots of ``shift_mode`` in order. Slot ``index`` is the scheduler unit.
    """
    windows = _SHIFT_WINDOWS.get(shift_mode)
    if windows is None:
        raise ValueError(f"Unknown shift mode: {shift_mode}")

    start = _parse_date(start_date)
    end = _parse_date(end_date)
    if end < start:
        raise ValueError("end_date must be on or after start_date")

    skip = {_parse_date(d) for d in (skipped_dates or [])}
    extra = {_parse_date(d) for d in (extra_workdays or [])}

    slots: list[Slot] = []
    day = start
    index = 0
    while day <= end:
        is_weekend = day.weekday() >= 5  # 5=Sat, 6=Sun
        working = day in extra or (day not in skip and (include_weekends or not is_weekend))
        if working:
            for shift_code, start_hhmm, end_hhmm in windows:
                # One slot per hour within the shift window.
                hour_start = _combine(day, start_hhmm)
                shift_end = _combine(day, end_hhmm)
                while hour_start < shift_end:
                    hour_end = hour_start + timedelta(hours=1)
                    slots.append(
                        Slot(
                            index=index,
                            day=day,
                            shift_code=shift_code,
                            start_at=hour_start,
                            end_at=hour_end,
                        )
                    )
                    index += 1
                    hour_start = hour_end
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


def earliest_index_on_or_after(slots: list[Slot], day: str) -> int | None:
    """First slot index whose day is on or after ``day`` (its target-or-later
    lower bound). None if no working slot falls on/after that date.

    Used for soft target dates: a PI request may drift to a later working day
    (e.g. when its target day is taken by FV), but never earlier (ADR-024).
    """
    target = _parse_date(day)
    candidates = [s.index for s in slots if s.day >= target]
    return min(candidates) if candidates else None


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
