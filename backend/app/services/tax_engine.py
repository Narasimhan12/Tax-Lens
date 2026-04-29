from __future__ import annotations

from dataclasses import dataclass

from app.models.schemas import BracketSegment, CompanyTaxInput, TaxComputation

PASS_THROUGH_ENTITIES = {"S-Corp", "LLC", "Partnership"}

FEDERAL_BRACKETS_2024 = [
    (0, 11600, 0.10),
    (11600, 47150, 0.12),
    (47150, 100525, 0.22),
    (100525, 191950, 0.24),
    (191950, 243725, 0.32),
    (243725, 609350, 0.35),
    (609350, None, 0.37),
]

STATE_RATES = {
    "CA": {"C-Corp": 0.0884, "PassThrough": 0.0930},
    "NY": {"C-Corp": 0.0650, "PassThrough": 0.1090},
    "TX": {"C-Corp": 0.0, "PassThrough": 0.0},
    "FL": {"C-Corp": 0.0550, "PassThrough": 0.0},
    "IL": {"C-Corp": 0.0950, "PassThrough": 0.0495},
    "WA": {"C-Corp": 0.0, "PassThrough": 0.0},
    "PA": {"C-Corp": 0.0899, "PassThrough": 0.0307},
    "OH": {"C-Corp": 0.0, "PassThrough": 0.0},
    "MA": {"C-Corp": 0.0800, "PassThrough": 0.0500},
    "NJ": {"C-Corp": 0.0900, "PassThrough": 0.1075},
}


@dataclass
class TaxEngine:
    def compute(self, company: CompanyTaxInput) -> TaxComputation:
        trace: list[str] = []
        federal_taxable_income = max(company.gross_income - company.deductions, 0)
        trace.append(f"Federal taxable income: max({company.gross_income} - {company.deductions}, 0)")

        if company.entity_type in PASS_THROUGH_ENTITIES:
            qbi_deduction = 0.2 * federal_taxable_income
            trace.append("QBI deduction applied at 20% for pass-through entity.")
        else:
            qbi_deduction = 0
            trace.append("No QBI deduction for C-Corp.")

        adjusted_federal_taxable_income = max(federal_taxable_income - qbi_deduction, 0)

        nol_cap = 0.8 * adjusted_federal_taxable_income
        nol_used = min(company.nol_carryforward, nol_cap)
        trace.append(f"NOL used: min({company.nol_carryforward}, 80% of {adjusted_federal_taxable_income})")

        final_federal_taxable_income = max(adjusted_federal_taxable_income - nol_used, 0)

        if company.entity_type == "C-Corp":
            federal_tax_before_credits = final_federal_taxable_income * 0.21
            bracket_breakdown: list[BracketSegment] = []
            trace.append("Federal tax for C-Corp calculated at flat 21%.")
        else:
            federal_tax_before_credits, bracket_breakdown = self._compute_progressive_tax(final_federal_taxable_income)
            trace.append("Federal tax for pass-through calculated with 2024 individual brackets.")

        federal_tax_after_credits = max(federal_tax_before_credits - company.credits, 0)
        trace.append(f"Credits applied to federal tax only: max({federal_tax_before_credits} - {company.credits}, 0)")

        state_taxable_income = max(company.gross_income - company.deductions, 0)
        state_rate = self._get_state_rate(company.state_code, company.entity_type)
        state_tax = state_taxable_income * state_rate

        if company.state_code == "CA" and state_tax < 800:
            state_tax = 800
            trace.append("California minimum franchise tax enforced at $800.")

        total_tax = federal_tax_after_credits + state_tax
        effective_tax_rate_percent = (total_tax / company.gross_income * 100) if company.gross_income > 0 else 0

        return TaxComputation(
            company_name=company.company_name,
            federal_taxable_income=round(federal_taxable_income, 2),
            qbi_deduction=round(qbi_deduction, 2),
            adjusted_federal_taxable_income=round(adjusted_federal_taxable_income, 2),
            nol_used=round(nol_used, 2),
            final_federal_taxable_income=round(final_federal_taxable_income, 2),
            federal_tax_before_credits=round(federal_tax_before_credits, 2),
            federal_tax_after_credits=round(federal_tax_after_credits, 2),
            state_taxable_income=round(state_taxable_income, 2),
            state_rate=state_rate,
            state_tax=round(state_tax, 2),
            total_tax=round(total_tax, 2),
            effective_tax_rate_percent=round(effective_tax_rate_percent, 2),
            bracket_breakdown=bracket_breakdown,
            rule_trace=trace,
        )

    def compare_state(self, company: CompanyTaxInput, new_state: str) -> dict:
        baseline = self.compute(company)
        moved = company.model_copy(update={"state_code": new_state})
        moved_calc = self.compute(moved)
        benefit = round(baseline.total_tax - moved_calc.total_tax, 2)
        return {
            "company_name": company.company_name,
            "from_state": company.state_code,
            "to_state": new_state,
            "total_tax_current": baseline.total_tax,
            "total_tax_new": moved_calc.total_tax,
            "tax_benefit": benefit,
            "federal_tax_current": baseline.federal_tax_after_credits,
            "federal_tax_new": moved_calc.federal_tax_after_credits,
            "state_tax_current": baseline.state_tax,
            "state_tax_new": moved_calc.state_tax,
        }

    def _compute_progressive_tax(self, income: float) -> tuple[float, list[BracketSegment]]:
        total = 0.0
        breakdown: list[BracketSegment] = []
        remaining = income

        for lower, upper, rate in FEDERAL_BRACKETS_2024:
            if remaining <= 0:
                break

            cap = upper if upper is not None else income
            segment_width = cap - lower if upper is not None else max(income - lower, 0)
            taxable_amount = min(max(remaining, 0), segment_width)
            segment_tax = taxable_amount * rate
            total += segment_tax
            remaining -= taxable_amount

            breakdown.append(
                BracketSegment(
                    rate=rate,
                    lower_bound=lower,
                    upper_bound=upper,
                    taxable_amount=round(taxable_amount, 2),
                    tax_for_segment=round(segment_tax, 2),
                )
            )

        return total, breakdown

    @staticmethod
    def _get_state_rate(state_code: str, entity_type: str) -> float:
        state = STATE_RATES.get(state_code)
        if not state:
            raise ValueError(f"Unsupported state code: {state_code}")
        if entity_type == "C-Corp":
            return state["C-Corp"]
        return state["PassThrough"]
