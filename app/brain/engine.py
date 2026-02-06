# -------------brain- engine---------->
# Design Rules (Very Important)
# This engine must be:
# Pure logic
# Stateless
# Deterministic
# Model-agnostic

# It should NOT:
# Touch FastAPI
# Mutate session
# Log
# Access OS


from enum import Enum
from typing import Dict
from app.brain.trace import DecisionTrace

class DecisionType(str, Enum):
    RESPOND = "respond"
    CLARIFY = "clarify"
    REFUSE = "refuse"
    
class DecisionEngine:
    """
    Central decision-making unit for the Local LLM Brain.

    Responsibilities:
    - Decide whether to respond, ask clarification, or refuse
    - Enforce clarification limits
    - Remain deterministic and explainable

    This engine does NOT:
    - Call models
    - Access memory
    - Interact with APIs
    """
    MAX_CLARIFICATIONS = 3
    
    # this is for whole class not instance so..
    @staticmethod
    def is_ambigous(message: str) -> bool:
        """
        Rule-based ambiguity detection.
        This will later be replaced or augmented by a model.
        """
        if not message:
            return True
        
        # too short -> ambigous
        if len(message) < 5:
            return True
        
        vague_phrases = {
            "do it",
            "this",
            "that",
            "something",
            "anything",
            "help",
            "run",
        }
        return any(phrase in message for phrase in vague_phrases)
    
    @classmethod
    def decide(cls, message:str, clarification_count: int) -> Dict:
        """
        Core decision pipeline.

        Input:
        - message: user input
        - clarification_count: number of clarifications already asked

        Output:
        - decision
        - reason
        - response
        - confidence
        """
        trace = DecisionTrace()
        
        
        trace.add_step("Received user message")
        trace.add_step(f"Message length: {len(message)} characters")

        if not message.strip():
            trace.add_rule("EMPTY_INPUT")
            trace.add_step("Message is empty")

        # Rule 1 : Clarification limit exceeded -> refuse
        if clarification_count >= 3:
            trace.add_rule("MAX_CLARIFICATION_REACHED")
            trace.add_step("Clarification limit exceeded")

            return {
                "decision": DecisionType.REFUSE,
                "reason": "Too many unclear requests",
                "response": "Please provide a clear instruction.",
                "confidence": 0.9,
                "trace": trace,
            }
            
        # Rule 2 : Ambigiuos input -> clarification ask
        if len(message.split()) < 3:
            trace.add_rule("AMBIGUOUS_INPUT")
            trace.add_step("Message too short to infer intent")

            return {
                "decision": DecisionType.CLARIFY,
                "reason": "Input is ambiguous or incomplete",
                "response": "Could you clarify what you want me to do?",
                "confidence": 0.4,
                "trace": trace,
            }

            
        # Rule 3 : input is clear - > respond (place holder)
        trace.add_rule("CLEAR_INTENT")
        trace.add_step("Input considered clear")

        return {
            "decision": DecisionType.RESPOND,
            "reason": "Clear user intent",
            "response": "Acknowledged.",
            "confidence": 0.7,
            "trace": trace,
        }

        