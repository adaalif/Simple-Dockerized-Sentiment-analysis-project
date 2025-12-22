from twikit import Client
from app.config import TWITTER_EMAIL, TWITTER_USERNAME, TWITTER_PASSWORD
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_tweets(topic: str, count: int = 100) -> list[str]:
    """
    Fetches recent tweets for a given topic using Twikit.

    Args:
        topic (str): The keyword or hashtag to search for.
        count (int): The number of tweets to attempt to fetch.

    Returns:
        list[str]: A list of tweet texts. Returns an empty list if an error occurs.
    """
    try:
        # Initialize Twikit client
        client = Client('en-US')
        # Login
        client.login(
            auth_info_1=TWITTER_EMAIL,
            auth_info_2=TWITTER_USERNAME,
            password=TWITTER_PASSWORD
        )
        
        logger.info(f"Searching Twitter with query: '{topic}'")

        # Search for tweets
        tweets = client.search_tweet(topic, 'Top')

        # Filter out retweets and limit the count
        tweet_texts = [
            tweet.text for tweet in tweets if not tweet.text.startswith('RT @')
        ][:count]
        
        if tweet_texts:
            logger.info(f"Successfully fetched {len(tweet_texts)} tweets.")
            return tweet_texts
        else:
            logger.info("No tweets found for the given topic.")
            return []

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return []

if __name__ == '__main__':
    # Example usage for direct execution (for testing purposes)
    # Make sure your .env file is populated with Twikit credentials
    search_topic = "Python programming"
    tweets = get_tweets(search_topic, count=15)
    
    if tweets:
        for i, tweet_text in enumerate(tweets, 1):
            print(f"--- Tweet {i} ---\n{tweet_text}\n")
    else:
        print("Could not fetch any tweets.")

