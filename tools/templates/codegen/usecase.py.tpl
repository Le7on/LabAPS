"""{{NAME_TITLE}} use case.

One business action, one transaction boundary (the Unit of Work). Coordinates
domain behaviour; contains no business rules, SQL or ORM logic (Use Case
Template, chapters 3-4).
"""

from __future__ import annotations


class {{NAME_PASCAL}}UseCase:
    def __init__(self, uow_factory):
        self._uow_factory = uow_factory

    def execute(self) -> dict:
        # Standard flow: validate -> load aggregate -> invoke domain ->
        # (invoke engine) -> persist -> return DTO.
        with self._uow_factory() as uow:  # noqa: F841
            # aggregate = uow.<repository>.get(...)
            # aggregate.<behaviour>()
            # uow.<repository>.save(aggregate)
            result: dict = {}

        return result
