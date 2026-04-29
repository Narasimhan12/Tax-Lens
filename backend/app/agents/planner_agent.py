from __future__ import annotations

from app.models.schemas import ChatRequest


class PlannerAgent:
    """Classifies user intent and selects workflow path."""

    def plan(self, request: ChatRequest) -> str:
        q = request.question.lower()
        if any(keyword in q for keyword in ["move", "relocate", "from", "to", "benefit", "compare state"]):
            return "state_comparison"
        if any(keyword in q for keyword in ["federal tax", "state tax", "total tax", "effective", "calculate"]):
            return "single_company_tax"
        return "reasoning"
