from client_support.contracts.policy import PolicyContext, PolicyDecision, PolicyResult

class PolicyEngine:
    """Deterministic safety gate. The agent can propose; it cannot authorize."""

    def evaluate(self, context: PolicyContext) -> PolicyResult:
        reasons: list[str] = []
        if context.identity_resolution_method == "fuzzy":
            reasons.append("identity_resolved_by_fuzzy_match")
        if context.category_automation_level != "full":
            reasons.append("category_not_fully_automated")
        if context.has_side_effect and context.proposed_action != "none":
            reasons.append("side_effecting_action_requires_explicit_policy")

        if reasons:
            return PolicyResult(decision=PolicyDecision.HUMAN_REVIEW, reasons=reasons)
        return PolicyResult(decision=PolicyDecision.ALLOW, reasons=[])
