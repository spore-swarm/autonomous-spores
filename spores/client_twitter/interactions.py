from typing import List
from spores.client_twitter.client import TwitterClient
from spores.core.runtime import AgentRuntime
from spores.client_twitter.types import Tweet
from datetime import datetime
from spores.core.utils import string_to_uuid
import os
import asyncio
from spores.core.context import compose_context

TWITTER_MESSAGE_HANDLER_TEMPLATE = """
# About {{agent_name}} (@{{twitter_user_name}}):
{{bio}}
{{lore}}
{{topics}}

{{characterPostExamples}}

{{post_directions}}

Recent interactions between {{agent_name}} and other users:
{{recentPostInteractions}}

{{recentPosts}}

# Task: Generate a post/reply in the voice, style and perspective of {{agent_name}} (@{{twitter_user_name}}) while using the thread of tweets as additional context:
Current Post:
{{current_post}}

Thread of Tweets You Are Replying To:
{{formattedConversation}}
"""

class InteractionClient:
    def __init__(self, client: TwitterClient, runtime: AgentRuntime):
        self.client = client
        self.runtime = runtime
        self.last_checked_tweet_id = None
        self.id: str = None
        self.username: str = None

    async def start(self):
         while True:
             await self.handle_twitter_interactions()
             poll_interval = int(os.getenv("TWITTER_POLL_INTERVAL") or 120)
             await asyncio.sleep(poll_interval)

    async def handle_twitter_interactions(self):
        """Handle Twitter interactions"""

        try:
            print("Checking Twitter interactions start")

            self.last_checked_tweet_id = await self.client.load_latest_checked_tweet_id()
            
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

    async def process_new_tweet(self, tweet: Tweet):
        """Process a new tweet"""
        print(f"Processing new tweet: {tweet.permanent_url}")

        # Generate room ID and user ID
        room_id = string_to_uuid(f"{tweet.conversation_id}-{self.runtime.agent.agent_id}")
        user_id = (self.runtime.agent.agent_id if tweet.user_id == self.id
                  else string_to_uuid(tweet.user_id))
        
        state = self.runtime.compose_state({
            'twitter_user_name': os.getenv("TWITTER_USER_NAME")
        })
        context = compose_context(state, TWITTER_MESSAGE_HANDLER_TEMPLATE)
        self.runtime.agent.short_memory.update(0, "system", context)
        response = self.runtime.process_message(user_id, room_id, tweet.text)

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