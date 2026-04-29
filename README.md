# Tax Lens Hackathon Starter (Angular + Python + Azure OpenAI + MongoDB)

This repository provides a complete hackathon-ready implementation for a **tax analysis widget**:

- **Deterministic tax computation engine** (100% rule-based, no AI for math)
- **Conversational reasoning layer** using **Azure OpenAI GPT-4.5**
- **Multi-agent backend** in Python/FastAPI
- **Angular widget frontend** for embedded chat + tax metrics
- **MongoDB session memory** for follow-up questions

## Repository Structure

- `backend/` FastAPI services, tax engine, agents, MongoDB memory, API routes
- `frontend/` Angular standalone widget app
- `docs/` architecture, developer guide, demo presentation

## Quick Start

### 1) Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env with your Azure OpenAI and MongoDB values
./run.sh
```

### 2) Frontend

```bash
cd frontend
npm install
npm start
```

Open: `http://localhost:4200`

Backend: `http://localhost:8000`

## API Endpoints

- `GET /health`
- `GET /api/v1/companies`
- `GET /api/v1/tax/{company_name}`
- `POST /api/v1/chat`

## Sample Chat Payload

```json
{
  "session_id": "demo-session-1",
  "question": "What is the federal tax for this company and why is it high?",
  "company_name": "Company 001",
  "compare_state_code": "TX"
}
```

## Important Design Rule

- AI is **only** used for explanation and what-if conversation.
- All tax numbers are computed by deterministic formulas in `tax_engine.py`.
