from __future__ import annotations

from app.models.schemas import CompanyTaxInput, TaxComputation
from app.services.tax_engine import TaxEngine


class CalculationAgent:
    def __init__(self) -> None:
        self.engine = TaxEngine()

    def run(self, company: CompanyTaxInput) -> TaxComputation:
        return self.engine.compute(company)

    def compare_states(self, company: CompanyTaxInput, new_state: str) -> dict:
        return self.engine.compare_state(company, new_state)
