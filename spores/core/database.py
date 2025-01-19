from typing import Any

from abc import ABC, abstractmethod

class DatabaseAdapter(ABC):
    db: Any

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def add_memory(self, role: str, content: str, agent_id: str, user_id: str):
        pass

    @abstractmethod
    def get_memories(self, params: dict):
        pass
