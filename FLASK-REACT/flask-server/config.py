import os
from dotenv import load_dotenv
<<<<<<< HEAD
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
=======

load_dotenv()

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
MONGO_URI = os.getenv("MONGO_URI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

>>>>>>> 61d5f0b3f3dff76ae0daaa7da2eba43bc48488f3
