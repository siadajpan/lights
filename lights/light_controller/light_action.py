from typing import List, Optional


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
