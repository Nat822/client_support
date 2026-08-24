from pathlib import Path


SRC = Path(__file__).parents[2] / "src" / "client_support"


def imports(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_domain_does_not_import_infrastructure() -> None:
    for path in (SRC / "domain").glob("*.py"):
        text = imports(path)
        assert "sqlalchemy" not in text
        assert "fastapi" not in text


def test_contracts_do_not_import_application_or_infrastructure() -> None:
    for path in (SRC / "contracts").glob("*.py"):
        text = imports(path)
        assert "sqlalchemy" not in text
        assert "fastapi" not in text
        assert "client_support.application" not in text
        assert "client_support.persistence" not in text


def test_policy_does_not_import_api_or_persistence() -> None:
    for path in (SRC / "policy").glob("*.py"):
        text = imports(path)
        assert "fastapi" not in text
        assert "client_support.persistence" not in text
