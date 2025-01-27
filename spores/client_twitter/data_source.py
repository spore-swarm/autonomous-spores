from abc import ABC, abstractmethod
from typing import List, Dict, Any
from spores.client_twitter.types import Profile, Tweet

class DataSource(ABC):
    """Abstract base class for retrieving Twitter data"""

    @abstractmethod
    async def get_recent_tweets(self, user_id: str, last_checked_tweet_id: str) -> List[Tweet]:
        """Get recent tweets by user ID
        
        Args:
            user_id: Twitter user ID
            
        Returns:
            List of all tweets as dictionaries
        """
        pass

    @abstractmethod
    async def get_mentioned_tweets(self, user_id: str, last_checked_tweet_id: str) -> List[Tweet]:
        """Get recent tweets mentioned by user ID
        
        Args:
            user_id: Twitter user ID
            
        Returns:
            List of all tweets as dictionaries
        """
        pass

    @abstractmethod
    async def get_profile(self, user_id: str) -> Profile:
        """Get user profile by user ID
        
        Args:
            user_id: Twitter user ID
            
        Returns:
            User profile information as dictionary
        """
        pass