from typing import Any

from abc import ABC, abstractmethod

class DatabaseAdapter(ABC):
    db: Any

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def create_memory(self, user_id:str, content: str, agent_id: str, room_id: str):
        pass
    
