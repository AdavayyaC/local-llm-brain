# Local LLM Brain

A CPU-only, production-style local LLM backend designed for traceable, explainable, and safe interaction.<br>
This project focuses on end-to-end system design, not just model inference — from API contracts to session lifecycle management.

## Project Goals
- Run fully on CPU (low overhead, low latency)
- No uncontrolled OS / kernel access
- Explicit user-controlled actions only
- Traceable and explainable outputs
- Production-quality backend structure
- Foundation for future agentic systems

## Status
- Day 1: API skeleton + logging + session-ready structure
- Day 2: Chat endpoint validation & session memory working


``` 
{
  "request_id": "...",
  "session_id": "...",
  "input_summary": "hello",
  "session_message_count": 1,
  "clarification_count": 0,
  "final_response": "Brain is alive. Model not loaded yet.",
  "confidence": 0.2
}

```
## Tech
- Python
- FastAPI
- uvicorn
- CPU-only inference (planned)
- In-memory session store (temporary)