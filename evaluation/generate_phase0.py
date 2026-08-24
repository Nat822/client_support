from pathlib import Path

import yaml


CASES = [
    {
        "id": "exact-order-tracking-001",
        "ticket": {"subject": "Where is my order?", "requester_email": "alice@example.com"},
        "identity_method": "exact_email",
        "expected": {"run_status": "completed", "policy_decision": "allow"},
    },
    {
        "id": "fuzzy-review-001",
        "ticket": {"subject": "My package has not arrived", "requester_email": "unknown@example.com"},
        "identity_method": "fuzzy",
        "expected": {"run_status": "human_review", "policy_decision": "human_review"},
    },
]


def main() -> None:
    target = Path(__file__).with_name("phase0-generated.yaml")
    target.write_text(yaml.safe_dump(CASES, sort_keys=False), encoding="utf-8")
    print(f"wrote {target}")


if __name__ == "__main__":
    main()
