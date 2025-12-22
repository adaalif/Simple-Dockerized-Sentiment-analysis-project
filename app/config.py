from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables from a .env file in the project root
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Twitter API Credentials for Twikit
TWITTER_EMAIL = os.getenv("TWITTER_EMAIL")
TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")

# Check if the essential Twikit credentials are provided
if not all([TWITTER_EMAIL, TWITTER_USERNAME, TWITTER_PASSWORD]):
    raise ValueError(
        "TWITTER_EMAIL, TWITTER_USERNAME, and TWITTER_PASSWORD must be set. "
        "Please check your .env file."
    )
