import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
MONGO_URI = os.getenv("MONGO_URI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

