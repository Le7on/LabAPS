"""{{NAME_TITLE}} repository.

Converts between the ORM model and the domain entity. Does not manage
transactions; the Unit of Work owns the session lifecycle.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from backend.modules.{{NAME_SNAKE}}.domain.entities.{{NAME_SNAKE}} import {{NAME_PASCAL}}


class {{NAME_PASCAL}}Repository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, entity: {{NAME_PASCAL}}) -> None:
        # Convert the domain entity to its ORM model and add it, e.g.:
        #   self.session.add(self._to_orm(entity))
        raise NotImplementedError

    def list(self) -> list[{{NAME_PASCAL}}]:
        raise NotImplementedError
