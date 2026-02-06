from fastapi import APIRouter
from pydantic import BaseModel
import uuid

from app.memory.session import SessionManager
from app.brain.engine import DecisionEngine, DecisionType

router = APIRouter(prefix="/chat", tags=["chat"])

# In-memory session manager (lives while server runs)
session_manager = SessionManager()


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


@router.post("/")
def chat(req: ChatRequest):
    request_id = str(uuid.uuid4())

    # 1. Get or create session
    session = session_manager.get_or_create_session(req.session_id)

    # 2. Run decision engine
    decision_result = DecisionEngine.decide(
        message=req.message,
        clarification_count=session.clarification_count,
    )

    decision = decision_result["decision"]
    trace = decision_result["trace"]

    # 3. Apply side effects via SessionManager
    if decision == DecisionType.CLARIFY:
        session_manager.increment_clarification(session)

    elif decision == DecisionType.RESPOND:
        session_manager.add_message(session, req.message)

    # 4. API response (trace included)
    return {
        "request_id": request_id,
        "session_id": session.session_id,
        "decision": decision,
        "reason": decision_result["reason"],
        "response": decision_result["response"],
        "clarification_count": session.clarification_count,
        "confidence": decision_result["confidence"],
        "trace": trace.to_dict(),
    }
