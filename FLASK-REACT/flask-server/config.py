import os
from pymongo import MongoClient
from dotenv import load_dotenv
from google.cloud import speech
from google.oauth2.service_account import Credentials

load_dotenv()
print(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
mongo_client = MongoClient(MONGO_URI)
db = mongo_client.get_default_database()

# Google Cloud setup
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
gcloud_creds = Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)
speech_client = speech.SpeechClient(credentials=gcloud_creds)