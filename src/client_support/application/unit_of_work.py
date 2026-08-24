from collections.abc import Callable
from typing import Protocol


class Transaction(Protocol):
    def commit(self) -> None: ...
    def rollback(self) -> None: ...


class UnitOfWork:
    """Small explicit transaction boundary for one application operation."""

    def __init__(self, session_factory: Callable[[], Transaction]) -> None:
        self._session_factory = session_factory
        self.session: Transaction | None = None

    def __enter__(self) -> Transaction:
        self.session = self._session_factory()
        return self.session

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        if self.session is None:
            return
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
