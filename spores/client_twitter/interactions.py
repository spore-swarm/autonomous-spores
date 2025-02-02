from spores.client_twitter.client import TwitterClient
from spores.core.runtime import AgentRuntime
from spores.client_twitter.types import Tweet

class InteractionClient:
    def __init__(self, client: TwitterClient, runtime: AgentRuntime):
        self.client = client
        self.runtime = runtime
        self.last_checked_tweet_id = None
        self.id: str = None
        self.username: str = None    

    @staticmethod
    def format_tweet(tweet: Tweet) -> str:
        """Format tweet"""
        return f"""  ID: {tweet.id}
  From: {tweet.name} (@{tweet.username})
  Text: {tweet.text}"""    