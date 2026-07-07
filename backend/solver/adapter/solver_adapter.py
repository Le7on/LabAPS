"""Solver Adapter interface.

The stable contract between the Scheduling Engine and any optimization backend.
Only implementations of this interface may import OR-Tools. Input is a
SchedulingModel; output is a SchedulingSolution. Business entities never cross
this boundary (Solver Model, architecture rules 18.1-18.3).
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from backend.engines.scheduling.scheduling_model import SchedulingModel, SchedulingSolution


class SolverAdapter(ABC):
    @abstractmethod
    def solve(self, model: SchedulingModel) -> SchedulingSolution:
        """Solve the scheduling model and return a solution."""
        raise NotImplementedError
