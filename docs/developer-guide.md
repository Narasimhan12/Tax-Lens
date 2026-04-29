# Developer Guide

## Prerequisites

- Python 3.11+
- Node.js 20+
- npm 10+
- MongoDB Atlas (or local MongoDB)
- Azure OpenAI resource with GPT-4.5 deployment

## Environment Variables (Backend)

Set in `backend/.env`:

- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_API_VERSION` (default `2024-10-21`)
- `AZURE_OPENAI_DEPLOYMENT` (name of your GPT-4.5 deployment)
- `MONGODB_URI`
- `MONGODB_DB_NAME`
- `DATASET_PATH`

## Package Installation

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Running Locally

### Run Backend

```bash
cd backend
source .venv/bin/activate
./run.sh
```

### Run Frontend

```bash
cd frontend
npm start
```

## Extending Tax Logic

Primary file:
- `backend/app/services/tax_engine.py`

Add deterministic rules there and keep them separated from LLM logic.

## MongoDB Memory Schema

Collection: `chat_sessions`

Document shape (simplified):

```json
{
  "session_id": "abc123",
  "history": [
    {"role": "user", "content": "...", "timestamp": "..."},
    {"role": "assistant", "content": "...", "metadata": {"company_name": "Company 001"}}
  ],
  "created_at": "...",
  "updated_at": "..."
}
```

## Production Notes

- Add auth (JWT / API key) before public deployment.
- Restrict CORS origins.
- Add request rate limiting.
- Add structured logging and observability.
- Add automated tests for every tax rule.
