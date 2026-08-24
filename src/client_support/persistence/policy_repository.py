from uuid import UUID

from sqlalchemy.orm import Session

from client_support.application.policy_audit import PolicyDecisionRecord
from client_support.persistence.models import PolicyDecisionModel


class SqlAlchemyPolicyDecisionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, record: PolicyDecisionRecord) -> None:
        self.session.add(
            PolicyDecisionModel(
                id=record.id,
                run_id=record.run_id,
                decision=record.decision.value,
                reason=record.reason,
                policy_version=record.policy_version,
                created_at=record.created_at,
            )
        )

    def list_for_run(self, run_id: UUID) -> list[PolicyDecisionModel]:
        return list(
            self.session.query(PolicyDecisionModel)
            .filter(PolicyDecisionModel.run_id == run_id)
            .order_by(PolicyDecisionModel.created_at)
            .all()
        )
