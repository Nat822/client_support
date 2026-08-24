from client_support.application.unit_of_work import UnitOfWork


class FakeTransaction:
    def __init__(self) -> None:
        self.commits = 0
        self.rollbacks = 0

    def commit(self) -> None:
        self.commits += 1

    def rollback(self) -> None:
        self.rollbacks += 1


def test_unit_of_work_commits_on_success() -> None:
    transaction = FakeTransaction()
    with UnitOfWork(lambda: transaction):
        pass
    assert transaction.commits == 1
    assert transaction.rollbacks == 0


def test_unit_of_work_rolls_back_on_error() -> None:
    transaction = FakeTransaction()
    try:
        with UnitOfWork(lambda: transaction):
            raise RuntimeError("boom")
    except RuntimeError:
        pass
    assert transaction.commits == 0
    assert transaction.rollbacks == 1
