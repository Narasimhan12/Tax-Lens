# Demo Presentation: Tax Lens AI Widget

## Slide 1 — Problem
- Finance teams need quick tax visibility across entities/states.
- Traditional tools are rigid and not conversational.
- Risk: AI hallucinations if AI computes numbers.

## Slide 2 — Our Approach
- Deterministic, rule-based tax engine for 100% numeric correctness.
- GPT-4.5 only for explanation and scenario narration.
- Session memory via MongoDB for natural follow-up Q&A.

## Slide 3 — Architecture
- Angular widget UI
- FastAPI multi-agent backend
- TaxEngine (rules)
- MongoDB memory
- Azure OpenAI reasoning layer

## Slide 4 — Multi-Agent Flow
1. PlannerAgent classifies intent.
2. CalculationAgent computes values.
3. ReasoningAgent explains values.
4. Orchestrator persists memory and returns response.

## Slide 5 — Tax Rules Implemented
- Federal taxable income, QBI, NOL cap, federal rates, credits
- State tax table and CA minimum franchise tax
- Effective tax rate and total tax outputs

## Slide 6 — Live Demo Script
1. Ask: "What is federal tax for Company 001?"
2. Ask follow-up: "Why is it high?"
3. Ask scenario: "What if moved from CA to TX?"
4. Show tax benefit output and explanation.

## Slide 7 — Why It Wins Hackathon
- Correctness-first architecture
- Explainable AI with strict guardrails
- Easy to demo and easy to extend
- Clear enterprise path (auditability + compliance)

## Slide 8 — Next Steps
- Add auth + RBAC
- CSV upload for customer data
- Downloadable PDF tax explanation reports
- Deeper entity-specific state rule packs
