from __future__ import annotations

import json

from app.services.llm_service import AzureLLMService


class ReasoningAgent:
    def __init__(self) -> None:
        self.llm = AzureLLMService()

    def explain(
        self,
        question: str,
        computation: dict | None,
        comparison: dict | None,
        history: list[dict],
    ) -> str:
        system_prompt = (
            "You are a tax explanation assistant. Never invent tax values. "
            "Use only provided computation JSON. Tax calculations are deterministic and rule-based. "
            "If user asks outside given rules, say limitation clearly."
        )
        user_prompt = (
            f"User question: {question}\n"
            f"Computation: {json.dumps(computation, default=str)}\n"
            f"Comparison: {json.dumps(comparison, default=str)}\n"
            f"Recent history: {json.dumps(history, default=str)}\n"
            "Provide concise explanation with 3 sections: Answer, Why, Next What-if."
        )
        return self.llm.explain(system_prompt, user_prompt)
