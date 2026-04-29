from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


EntityType = Literal["C-Corp", "S-Corp", "LLC", "Partnership"]


class CompanyTaxInput(BaseModel):
    company_name: str = Field(alias="CompanyName")
    gross_income: float = Field(alias="GrossIncome")
    deductions: float = Field(alias="Deductions")
    entity_type: EntityType = Field(alias="EntityType")
    state_code: str = Field(alias="StateCode")
    tax_year: int = Field(alias="TaxYear")
    nol_carryforward: float = Field(alias="NOLCarryforward")
    estimated_payments: float = Field(alias="EstimatedPayments")
    credits: float = Field(alias="Credits")


class BracketSegment(BaseModel):
    rate: float
    lower_bound: float
    upper_bound: float | None
    taxable_amount: float
    tax_for_segment: float


class TaxComputation(BaseModel):
    company_name: str
    federal_taxable_income: float
    qbi_deduction: float
    adjusted_federal_taxable_income: float
    nol_used: float
    final_federal_taxable_income: float
    federal_tax_before_credits: float
    federal_tax_after_credits: float
    state_taxable_income: float
    state_rate: float
    state_tax: float
    total_tax: float
    effective_tax_rate_percent: float
    bracket_breakdown: list[BracketSegment] = Field(default_factory=list)
    rule_trace: list[str] = Field(default_factory=list)


class ChatRequest(BaseModel):
    session_id: str
    question: str
    company_name: str | None = None
    compare_state_code: str | None = None


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    computation: TaxComputation | None = None
    comparison: dict[str, Any] | None = None


class SessionMemory(BaseModel):
    session_id: str
    history: list[dict[str, Any]] = Field(default_factory=list)
