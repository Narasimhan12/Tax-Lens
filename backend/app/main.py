from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat_orchestrator import ChatOrchestrator
from app.services.company_repository import CompanyRepository
from app.services.tax_engine import TaxEngine

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repo = CompanyRepository()
engine = TaxEngine()
orchestrator = ChatOrchestrator()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "environment": settings.environment}


@app.get(f"{settings.api_prefix}/companies")
def companies() -> dict:
    return {"companies": repo.list_company_names()}


@app.get(f"{settings.api_prefix}/tax/{{company_name}}")
def tax(company_name: str) -> dict:
    try:
        company = repo.get_company(company_name)
        computation = engine.compute(company)
        return computation.model_dump()
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post(f"{settings.api_prefix}/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        return orchestrator.process(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
