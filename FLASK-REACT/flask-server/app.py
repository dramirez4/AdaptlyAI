import os
from flask_cors import CORS
from flask import Flask, request, jsonify
from google.cloud import speech_v1 as speech
from flask_pymongo import PyMongo
from pydub import AudioSegment
import config  # This imports the config we set up for Google Cloud and MongoDB.

app = Flask(__name__)
<<<<<<< HEAD

# Load your pre-trained emotion classification model
model_path = '/Users/davidramirez/Desktop/AdaptlyAI/AdaptlyAI/model.h5'  # Update with the correct path
classifier = load_model(model_path)
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Enable CORS for your app
=======
>>>>>>> 06f1e05fcef94bed380096e60091f17dd8740f98
CORS(app)

from views import bp as views_bp
app.register_blueprint(views_bp)

# MongoDB Configuration
app.config["MONGO_URI"] = config.MONGO_URI
mongo = PyMongo(app)

def process_audio_file(file_path):
    """Process audio file to ensure it's in mono and 16kHz sample rate."""
    audio = AudioSegment.from_wav(file_path)
    
    # Convert stereo to mono
    if audio.channels > 1:
        audio = audio.set_channels(1)
    
    # Set sample rate to 16kHz
    audio = audio.set_frame_rate(16000)
    
    # Save processed audio
    processed_path = "processed_" + file_path.split("/")[-1]
    audio.export(processed_path, format="wav")
    
    return processed_path

def speech_to_text(audio_path):
    client = speech.SpeechClient()

    with open(audio_path, 'rb') as f:
        audio_data = f.read()

    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        transcript = result.alternatives[0].transcript
        return transcript 

@app.route('/speech_to_text', methods=['POST'])
def process_audio():
<<<<<<< HEAD
    # This is where you'll receive the audio file from the frontend.
    # # For now, let's just use a test file path.
    transcript = speech_to_text("path/to/audio/file")
    return jsonify({'transcript': transcript})
    pass
=======
    if 'file' not in request.files:
        print("No file in request.files")
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        print("No filename specified")
        return jsonify({'error': 'No selected file'}), 400

    # Saving file temporarily for processing
    audio_path = os.path.join("temporary_storage", file.filename)
    file.save(audio_path)

    # Process the audio to ensure it fits Google STT requirements
    processed_audio_path = process_audio_file(audio_path)

    transcript = speech_to_text(processed_audio_path)
    os.remove(audio_path)  # Remove the original temporary file after processing
    os.remove(processed_audio_path)  # Remove the processed temporary file after processing

    return jsonify({'transcript': transcript})
>>>>>>> 06f1e05fcef94bed380096e60091f17dd8740f98

if __name__ == "__main__":
    app.run(debug=True)