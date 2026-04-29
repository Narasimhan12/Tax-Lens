# Architecture

## High-Level Components

1. **Angular Widget (frontend)**
   - Captures user input, selected company, optional comparison state.
   - Calls backend chat endpoint.
   - Renders assistant response and latest deterministic tax metrics.

2. **FastAPI Backend**
   - Company dataset loader (`CompanyRepository`)
   - Deterministic tax engine (`TaxEngine`)
   - Multi-agent orchestration (`ChatOrchestrator`)
   - Session memory persistence (`MemoryStore`, MongoDB)
   - LLM reasoning service (`AzureLLMService`)

3. **MongoDB**
   - Stores user and assistant messages per `session_id`
   - Enables follow-up context and continuity.

4. **Azure OpenAI GPT-4.5**
   - Generates natural-language explanations and what-if narratives.
   - Never computes tax values directly.

## Multi-Agent Pattern

- **PlannerAgent**: intent classification (calculation vs state comparison vs reasoning)
- **CalculationAgent**: invokes deterministic tax engine
- **ReasoningAgent**: prompts Azure OpenAI with computed JSON + history
- **ChatOrchestrator**: sequencing + state management

## Data Flow

1. Frontend sends chat payload.
2. Backend logs user turn in MongoDB.
3. Planner chooses workflow.
4. Calculation agent computes tax outputs from rules.
5. Reasoning agent builds explanation from computed outputs.
6. Assistant turn is stored in MongoDB.
7. Frontend displays answer + computed metrics.
