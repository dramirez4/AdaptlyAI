import os
from dotenv import load_dotenv
load_dotenv("/Users/elijahumana/Documents/GitHub/AdaptlyAI/FLASK-REACT/flask-server/.env")

# Google Cloud setup

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
MONGO_URI = os.getenv("MONGO_URI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVEN_KEY = "fb1d27b5fb4d1ceb38083a558f24f1cd"


# print(ELEVEN_KEY)  # This should print the value of your key or 'None' if not set