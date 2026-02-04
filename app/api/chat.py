from fastapi import APIRouter
from pydantic import BaseModel
from app.memory.session import SessionManager
import uuid

router = APIRouter(prefix="/chat", tags=["chat"])


# this is will run till server runs
session_manager = SessionManager()


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

@router.post("/")
def chat(req: ChatRequest):
    request_id = str(uuid.uuid4())
    # session_id = req.session_id or str(uuid.uuid4())
    
    # ask session manager for session
    session = session_manager.get_or_create_session(req.session_id)
    
    # store user message
    session_manager.add_message(session,req.message)
    
    response_text = "Message received and stored in session memory."

    return {
        "request_id": request_id,
        "session_id": session.session_id,
        "input_summary": req.message,
        "session_message_count": len(session.messages),
        "clarification_count":session.clarification_count,
        "final_response": "Brain is alive. Model not loaded yet \n " + response_text,
        "confidence": 0.2
    }

 