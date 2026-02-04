from datetime import datetime
from typing import Dict, List
import uuid


class Session:
    """
    Represents a single conversation session.
    Holds only session-specific state.
    """

    def __init__(self, session_id: str | None = None):
        self.session_id: str = session_id or str(uuid.uuid4())
        self.messages: List[str] = []
        self.clarification_count: int = 0
        self.created_at: datetime = datetime.utcnow()
        self.last_accessed: datetime = self.created_at
        


class SessionManager:
    """
    Manages all active sessions in memory.
    Responsible for lifecycle, lookup, and cleanup.
    """

    def __init__(self):
        self._sessions: Dict[str, Session] = {}

    def get_or_create_session(self, session_id: str | None = None) -> Session:
        if session_id and session_id in self._sessions:
            session = self._sessions[session_id]
            session.last_accessed = datetime.utcnow()
            return session

        session = Session(session_id=session_id)
        self._sessions[session.session_id] = session
        return session
    

    def add_message(self, session: Session, message: str):
        session.messages.append(message)
        session.last_accessed = datetime.utcnow()
        

    def increment_clarification(self, session: Session):
        session.clarification_count += 1
        session.last_accessed = datetime.utcnow()
        

    def clear_session(self, session_id: str):
        if session_id in self._sessions:
            del self._sessions[session_id]
