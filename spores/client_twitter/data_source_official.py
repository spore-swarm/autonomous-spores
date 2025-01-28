import os
from typing import List, Dict, Any
from spores.client_twitter.data_source import DataSource
import tweepy

from spores.client_twitter.types import Profile, Tweet


# Your app's API/consumer key and secret can be found under the Consumer Keys
# section of the Keys and Tokens tab of your app, under the
# Twitter Developer Portal Projects & Apps page at
# https://developer.twitter.com/en/portal/projects-and-apps
consumer_key = os.getenv("TWITTER_SDK_CONSUMER_KEY")
consumer_secret = os.getenv("TWITTER_SDK_API_CONSUMER_SECRET")

bearer_token = os.getenv("TWITTER_SDK_BEARER_TOKEN")

# Your account's (the app owner's account's) access token and secret for your
# app can be found under the Authentication Tokens section of the
# Keys and Tokens tab of your app, under the
# Twitter Developer Portal Projects & Apps page at
# https://developer.twitter.com/en/portal/projects-and-apps
access_token = os.getenv("TWITTER_SDK_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_SDK_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)

client = tweepy.Client(bearer_token)

api = tweepy.API(auth, wait_on_rate_limit=True)

class OfficialDataSource(DataSource):
    """Official Twitter API data source implementation"""
    
    def get_recent_tweets(self, user_id: str, last_checked_tweet_id: str) -> List[Tweet]:
        response = client.get_users_tweets(
            id=user_id,
            max_results=20,
            expansions=["author_id", "in_reply_to_user_id"],
            tweet_fields=["conversation_id", "created_at"],
            user_fields=["name", "username"],
            since_id=last_checked_tweet_id
        )
        
        print("get_recent_tweets called successfully, last_checked_tweet_id:", last_checked_tweet_id)
        
        for tweet in response.data:
            print(f"Tweet ID: {tweet.id}, Created at: {tweet.created_at}")
            print(f"Text: {tweet.text}")


        for user in response.includes["users"]:
            print(f"User: {user.name} (@{user.username})")

        return response.data

    def get_mentioned_tweets(self, user_id: str, last_checked_tweet_id: str) -> List[Tweet]:
        response = client.get_users_mentions(
            id=user_id,
            max_results=20,
            expansions=["author_id", "in_reply_to_user_id"],
            tweet_fields=["conversation_id", "created_at"],
            user_fields=["name", "username"],
            since_id=last_checked_tweet_id
        )
        
        print("get_mentioned_tweets called successfully, last_checked_tweet_id:", last_checked_tweet_id)
        
        for tweet in response.data:
            print(f"Tweet ID: {tweet.id}, Created at: {tweet.created_at}")
            print(f"Text: {tweet.text}")


        for user in response.includes["users"]:
            print(f"User: {user.name} (@{user.username})")

        return response.data

    def get_profile(self, user_id: str) -> Profile:
        """Get user profile by user ID
        
        Args:
            user_id: Twitter user ID
            
        Returns:
            User profile information as dictionary
        """
        response = client.get_user(id=user_id, user_fields=["id", "name", "username", "bio"])
        
        print("get_profile called successfully, response:", response.data)

        return response.data