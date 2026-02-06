from typing import List
from datetime import datetime


class DecisionTrace:
    """
    Captures why and how a decision was made.
    """

    def __init__(self):
        self.timestamp = datetime.utcnow().isoformat()
        self.steps: List[str] = []
        self.rules_triggered: List[str] = []

    def add_step(self, step: str) -> None:
        self.steps.append(step)

    def add_rule(self, rule: str) -> None:
        self.rules_triggered.append(rule)

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "steps": self.steps,
            "rules_triggered": self.rules_triggered,
        }
