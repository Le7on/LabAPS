"""Unit of Work.

Encapsulates one transaction boundary (Development Guide, DI Strategy section 10:
"One Use Case = One Unit of Work"). Use cases enter the context, work through the
provided repositories, and the UoW commits on success or rolls back on error, then
always closes the session. This removes the repeated try/commit/rollback/close
boilerplate from every use case.

Read-only use cases may use the same context and simply not call commit.
"""

from __future__ import annotations

from types import TracebackType

from sqlalchemy.orm import Session

from backend.modules.execution.repository.execution_record_repository import (
    ExecutionRecordRepository,
)
from backend.modules.laboratory.repository.equipment_repository import (
    EquipmentRepository,
)
from backend.modules.laboratory.repository.project_repository import ProjectRepository
from backend.modules.laboratory.repository.staff_repository import StaffRepository
from backend.modules.laboratory.repository.workflow_definition_repository import (
    WorkflowDefinitionRepository,
)
from backend.modules.planning.repository.assignment_repository import (
    AssignmentRepository,
)
from backend.modules.planning.repository.demand_repository import DemandRepository
from backend.modules.planning.repository.plan_repository import PlanRepository
from backend.modules.planning.repository.workflow_instance_repository import (
    WorkflowInstanceRepository,
)


class UnitOfWork:
    def __init__(self, session_factory):
        self._session_factory = session_factory
        self.session: Session | None = None

    def __enter__(self) -> UnitOfWork:
        self.session = self._session_factory()
        self.plans = PlanRepository(self.session)
        self.assignments = AssignmentRepository(self.session)
        self.demands = DemandRepository(self.session)
        self.workflow_instances = WorkflowInstanceRepository(self.session)
        self.execution_records = ExecutionRecordRepository(self.session)
        self.equipment = EquipmentRepository(self.session)
        self.staff = StaffRepository(self.session)
        self.projects = ProjectRepository(self.session)
        self.workflow_definitions = WorkflowDefinitionRepository(self.session)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        try:
            if exc_type is None:
                self.session.commit()
            else:
                self.session.rollback()
        finally:
            self.session.close()
            self.session = None

    def commit(self) -> None:
        self.session.commit()
