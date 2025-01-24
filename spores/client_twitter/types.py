from dataclasses import dataclass
from typing import Optional


@dataclass
class Profile:
    id: str
    username: str
    bio: str

@dataclass
class Tweet:
    id: str
    text: str
    user_id: str
    username: str
    name: str
    conversation_id: str
    permanent_url: str
    timestamp: int
    in_reply_to_status_id: Optional[str] = None