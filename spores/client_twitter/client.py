from spores.core.runtime import AgentRuntime
from spores.client_twitter.types import Profile, Tweet
from typing import Dict, Optional, Any
from spores.client_twitter.data_source import DataSource
import os

class TwitterClient:
    def __init__(self, runtime: AgentRuntime, data_source: DataSource):
        self.runtime= runtime
        self.data_source = data_source
        self.last_checked_tweet_id: str = None
        self.profile: Profile = None

        ## todo: user db to store cache
        self.cached_tweets: Dict[str, Tweet] = {}
        self.cache_profile: Profile = None
        self.cached_latest_checked_tweet_id: str = None

    async def init(self) -> None:
        username = os.getenv("TWITTER_USER_NAME")
        await self.load_profile(username);
    
    async def cache_tweet(self, tweet: Tweet) -> None:
        self.cached_tweets[tweet.id] = tweet

    async def get_cached_tweet(self, tweet_id: str) -> Optional[Any]:
        return self.cached_tweets.get(tweet_id)

    async def get_tweet(self, tweet_id: str) -> Optional[Tweet]:
        tweet = self.cached_tweets[tweet_id]
        if not tweet:
            tweet = self.data_source.get_tweet(tweet_id)
        return tweet

    async def load_latest_checked_tweet_id(self):
        return self.runtime.cache_manager.get("latest_checked_tweet_id")

    async def cache_latest_checked_tweet_id(self, tweet_id: str) -> None:
        self.runtime.cache_manager.set("latest_checked_tweet_id", tweet_id)

    async def get_cached_profile(self, username: str) -> Optional[Profile]:
        return self.cache_profile

    async def cache_profile(self, profile: Profile) -> None:
        self.cache_profile = profile

    async def load_profile(self, username: str) -> Optional[Profile]:
        profile = await self.get_cached_profile(username)
        
        if not profile:
            profile = await self.data_source.get_profile(username)

        self.profile = profile;

        return profile    