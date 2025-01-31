
from typing import List, Dict, Any

from spores.client_twitter.data_source import DataSource
from spores.client_twitter.types import Profile, Tweet

class MockDataSource(DataSource):
    """Mock data source implementation, for testing"""
    
    def __init__(self):
        self.tweets: List[Tweet] = [Tweet(
            id="124",
            text="Hello, world!",
            user_id="456",
            username="Dobby",
            name="Dobby",
            conversation_id="789",
            permanent_url="https://twitter.com/Dobby/status/124",
            timestamp=1715731201,
            in_reply_to_status_id=None,
        ), Tweet(
            id="125",
            text="Hello, world!",
            user_id="456",
            username="Dobby",
            name="Dobby",
            conversation_id="789",
            permanent_url="https://twitter.com/Dobby/status/125",
            timestamp=1715731202,
            in_reply_to_status_id=None,
        )]
        self.mentioned_tweets: List[Tweet] = [
            Tweet(
                id="126",
                text="Hello, world!",
                user_id="4568",
                username="musk",
                name="musk",
                conversation_id=None,
                permanent_url="https://twitter.com/Dobby/status/126",
                timestamp=1715731203,
                in_reply_to_status_id=None,
            ), Tweet(
                id="127",
                text="Hello, world!",
                user_id="4569",
                username="elon",
                name="elon",
                conversation_id=None,
                permanent_url="https://twitter.com/Dobby/status/127",
                timestamp=1715731204,
                in_reply_to_status_id=None,
            )
        ]

    async def get_recent_tweets(self, user_id: str, last_checked_tweet_id: str) -> List[Tweet]:
        return self.tweets

    async def get_mentioned_tweets(self, user_id: str, last_checked_tweet_id: str) -> List[Tweet]:
        return self.mentioned_tweets

    async def get_profile(self, user_id: str) -> Profile:
        return {
            "id": "456",
            "username": "Dobby",
            "bio": "Hello, world!",
        }