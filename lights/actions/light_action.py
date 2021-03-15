import logging
from typing import List, Optional, Dict, Any


class LightAction:
    def __init__(self, method, args: Optional[List] = None):
        self.method = method
        self.arguments = args
        self._logger = logging.getLogger(self.__class__.__name__)

    def execute(self):
        self._logger.debug(f'Executing method {self.method} with args '
                           f'{self.arguments}')
        if self.arguments:
            self.method(*self.arguments)
        else:
            self.method()

    def __repr__(self):
        return f"LightAction: method: {self.method}, arguments: {self.arguments}"

    def evaluate_payload(self, payload: Dict[str, Any]) -> bool:
        raise NotImplementedError
