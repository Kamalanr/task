# Import OS module to access environment variables
import os

# Import dotenv to load variables from .env file
from dotenv import load_dotenv


# Load variables from .env file into environment
load_dotenv()


# Get Telegram bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN_env")

# Get admin chat ID and convert it into integer (important!)
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID_env"))

# Get OpenAI API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY_env")