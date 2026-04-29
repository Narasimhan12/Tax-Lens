from __future__ import annotations

from app.agents.calculation_agent import CalculationAgent
from app.agents.planner_agent import PlannerAgent
from app.agents.reasoning_agent import ReasoningAgent
from app.models.schemas import ChatRequest, ChatResponse
from app.services.company_repository import CompanyRepository
from app.services.memory_store import MemoryStore


class ChatOrchestrator:
    def __init__(self) -> None:
        self.repo = CompanyRepository()
        self.memory = MemoryStore()
        self.planner = PlannerAgent()
        self.calculator = CalculationAgent()
        self.reasoner = ReasoningAgent()

    def process(self, request: ChatRequest) -> ChatResponse:
        self.memory.append_message(request.session_id, "user", request.question)
        history = self.memory.get_history(request.session_id)

        plan = self.planner.plan(request)
        computation = None
        comparison = None
        selected_company = request.company_name

        if not selected_company:
            selected_company = self._resolve_company_from_history(history)

        if selected_company:
            company = self.repo.get_company(selected_company)
            computation = self.calculator.run(company)

            if plan == "state_comparison" and request.compare_state_code:
                comparison = self.calculator.compare_states(company, request.compare_state_code)

        answer = self.reasoner.explain(
            question=request.question,
            computation=computation.model_dump() if computation else None,
            comparison=comparison,
            history=history,
        )

        self.memory.append_message(
            request.session_id,
            "assistant",
            answer,
            metadata={
                "company_name": selected_company,
                "plan": plan,
                "comparison_state": request.compare_state_code,
            },
        )

        return ChatResponse(
            session_id=request.session_id,
            answer=answer,
            computation=computation,
            comparison=comparison,
        )

    @staticmethod
    def _resolve_company_from_history(history: list[dict]) -> str | None:
        for item in reversed(history):
            metadata = item.get("metadata", {})
            company_name = metadata.get("company_name")
            if company_name:
                return company_name
        return None
