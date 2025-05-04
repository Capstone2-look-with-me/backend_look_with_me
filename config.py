import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("assets/env/.env")

API_URL = os.getenv("API_URL")
