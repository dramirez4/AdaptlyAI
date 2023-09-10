import os
from pymongo import MongoClient
from dotenv import load_dotenv
from google.cloud import speech_v1 as speech
from google.oauth2.service_account import Credentials

# Set your MongoDB URI and Google Cloud credentials file path here
MONGO_URI = "mongodb+srv://elijah:<uQ5SkbPs41qmJy1m>@cluster0.8jay3.mongodb.net/Cluster0?retryWrites=true&w=majority"
GOOGLE_APPLICATION_CREDENTIALS = "/Users/davidramirez/Desktop/AdaptlyAI/AdaptlyAI/FLASK-REACT/flask-server/adaptlyai-GoogleCloudTextToSpeech.json"

# MongoDB setup
mongo_client = MongoClient(MONGO_URI)
# Specify the database name in the URI (if it's not included in the URI)
# For example, if the URI is mongodb+srv://elijah:<password>@cluster0.8jay3.mongodb.net/test
# You can specify the database name like this: db = mongo_client["test"]
db = mongo_client.get_default_database()

# Google Cloud setup
# Load Google Cloud credentials from the provided JSON key file
gcloud_creds = Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS)

# Create a Google Cloud Speech client with the loaded credentials
speech_client = speech.SpeechClient(credentials=gcloud_creds)


