from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Event(ABC):
    timestamp: datetime
    body: str

class Integration(ABC):

    @abstractmethod
    def __init__(self, **credentials) -> None:
        super().__init__()
        ...

    # @abstractmethod
    # def authenticate(self):
    #     ...
    
    # @abstractmethod
    # def get_events(self, start: datetime, end: datetime):
    #     ...
