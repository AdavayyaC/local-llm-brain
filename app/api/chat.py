from fastapi import APIRouter
from pydantic import BaseModel
import uuid

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

@router.post("/")
def chat(req: ChatRequest):
    request_id = str(uuid.uuid4())
    session_id = req.session_id or str(uuid.uuid4())

    return {
        "request_id": request_id,
        "session_id": session_id,
        "input_summary": req.message,
        "final_response": "Brain is alive. Model not loaded yet.",
        "confidence": 0.1
    }

# This is a stub — and that’s intentional