from typing import List
from src.integrations import Integration

class Summary:
    def __init__(self, *integrations: List[Integration]) -> None:
        self.integrations = dict()
        for integration in integrations:
            integration.authenticate()
            self.integrations[integration.__name__] = integration
