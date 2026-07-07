"""Scheduling Engine.

Orchestrates the scheduling pipeline: validate the Planning Problem, build the
Scheduling Model, solve it through the injected Solver Adapter, and rebuild
Assignments. Stateless; all collaborators are injected (Composition Root wires
the concrete Solver Adapter).
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.engines.planning.planning_problem import PlanningProblem
from backend.engines.planning.planning_problem_validator import PlanningProblemValidator
from backend.engines.scheduling.assignment_builder import Assignment, AssignmentBuilder
from backend.engines.scheduling.scheduling_model_builder import SchedulingModelBuilder
from backend.solver.adapter.solver_adapter import SolverAdapter


@dataclass(frozen=True, slots=True)
class ScheduleResult:
    assignments: tuple[Assignment, ...]
    makespan: int
    status: str
    feasible: bool


class SchedulingEngine:
    def __init__(
        self,
        solver_adapter: SolverAdapter,
        validator: PlanningProblemValidator | None = None,
        model_builder: SchedulingModelBuilder | None = None,
        assignment_builder: AssignmentBuilder | None = None,
    ):
        self._solver = solver_adapter
        self._validator = validator or PlanningProblemValidator()
        self._model_builder = model_builder or SchedulingModelBuilder()
        self._assignment_builder = assignment_builder or AssignmentBuilder()

    def schedule(self, problem: PlanningProblem) -> ScheduleResult:
        self._validator.validate(problem)
        model = self._model_builder.build(problem)
        solution = self._solver.solve(model)
        assignments = self._assignment_builder.build(solution, model)
        return ScheduleResult(
            assignments=assignments,
            makespan=solution.makespan,
            status=solution.status,
            feasible=solution.feasible,
        )
