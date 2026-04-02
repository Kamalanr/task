import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN_env")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID_env"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY_env")