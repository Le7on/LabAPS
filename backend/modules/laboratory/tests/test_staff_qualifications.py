"""Unit tests for staff qualification validity."""

from __future__ import annotations

from backend.modules.laboratory.domain.entities.staff import Staff


def test_qualification_with_no_expiry_is_always_valid():
    staff = Staff(staff_code="ST-1", name="A", qualifications={"gmp": None})
    assert "gmp" in staff.valid_qualifications("2026-07-08")


def test_qualification_valid_on_or_before_expiry():
    staff = Staff(staff_code="ST-1", name="A", qualifications={"gmp": "2026-12-31"})
    assert "gmp" in staff.valid_qualifications("2026-07-08")
    assert "gmp" in staff.valid_qualifications("2026-12-31")


def test_expired_qualification_is_excluded():
    staff = Staff(staff_code="ST-1", name="A", qualifications={"gmp": "2026-01-01"})
    assert staff.valid_qualifications("2026-07-08") == set()
