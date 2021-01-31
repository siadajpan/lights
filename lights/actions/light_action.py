from typing import List, Optional, Dict, Any


class LightAction:
    def __init__(self, method, args: Optional[List] = None, priority=5):
        self.method = method
        self.arguments = args
        self.priority = priority

    def execute(self):
        if self.arguments:
            self.method(*self.arguments)
        else:
            self.method()

    def __repr__(self):
        return f"LightAction: method: {self.method}, arguments: {self.arguments}"

    def evaluate_payload(self, payload: Dict[str, Any]) -> bool:
        raise NotImplementedError
