from typing import List
from spores.client_twitter.client import TwitterClient
from spores.core.runtime import AgentRuntime
from spores.client_twitter.types import Tweet
from datetime import datetime

class InteractionClient:
    def __init__(self, client: TwitterClient, runtime: AgentRuntime):
        self.client = client
        self.runtime = runtime
        self.last_checked_tweet_id = None
        self.id: str = None
        self.username: str = None    

    async def handle_twitter_interactions(self):
        """Handle Twitter interactions"""

        try:
            print("Checking Twitter interactions start")

            # Get blacklisted users
            user_blacklist = []

            # Get mentions
            tweet_candidates = await self.client.data_source.get_mentioned_tweets(
                self.username,
                self.last_checked_tweet_id
            )

            print(f"Tweet candidates successfully fetched >>>>> ")

            # Filter out own tweets and blacklisted users
            filtered_tweets = [
                tweet for tweet in tweet_candidates
                if tweet.user_id != self.id
                and tweet.username not in user_blacklist
            ]

            print("filtered_tweets", filtered_tweets)

            for tweet in filtered_tweets:
                if (not self.last_checked_tweet_id or
                    int(tweet.id) > self.last_checked_tweet_id):
                    await self.process_new_tweet(tweet)
                    self.last_checked_tweet_id = int(tweet.id)

            # Cache latest checked tweet ID
            await self.client.cache_latest_checked_tweet_id(self.last_checked_tweet_id)

        except Exception as e:
            print(f"Error handling Twitter interactions: {e}")
            
    @staticmethod
    def format_tweet(tweet: Tweet) -> str:
        """Format tweet"""
        return f"""  ID: {tweet.id}
  From: {tweet.name} (@{tweet.username})
  Text: {tweet.text}"""    
    
    @staticmethod
    def format_conversation(thread: List[Tweet]) -> str:
        """Format conversation thread"""
        return "\n\n".join(
            f"@{tweet.username} ({datetime.fromtimestamp(tweet.timestamp).strftime('%b %d, %I:%M %p')}): "
            f"{tweet.text}"
            for tweet in thread
        )    