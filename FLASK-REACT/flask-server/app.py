from views import bp as views_bp
import os
from flask_cors import CORS
from flask import Flask, request, jsonify
from google.cloud import speech_v1 as speech
from flask_pymongo import PyMongo
from pydub import AudioSegment
import config  # This imports the config set up for Google Cloud and MongoDB.
from gpt4_api import call_gpt4_to_extract_info

app = Flask(__name__)
CORS(app)  # Enable CORS for your app

# Load your pre-trained emotion classification model
# Update with the correct path
model_path = '/Users/davidramirez/Desktop/AdaptlyAI/AdaptlyAI/model.h5'
classifier = load_model(model_path)
emotion_labels = ['Angry', 'Disgust', 'Fear',
                  'Happy', 'Neutral', 'Sad', 'Surprise']

app.register_blueprint(views_bp)

# MongoDB Configuration
app.config["MONGO_URI"] = config.MONGO_URI
mongo = PyMongo(app)

def process_audio_file(file_path):
    audio = AudioSegment.from_wav(file_path)
    if audio.channels > 1:
        audio = audio.set_channels(1)
    audio = audio.set_frame_rate(16000)
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

    response = client.long_running_recognize(config=config, audio=audio).result()

    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)

    return ' '.join(transcripts)

@app.route('/speech_to_text', methods=['POST'])
def process_audio():
    if 'file' not in request.files:
        print("No file in request.files")
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        print("No filename specified")
        return jsonify({'error': 'No selected file'}), 400

    audio_path = os.path.join("temporary_storage", file.filename)
    file.save(audio_path)
    processed_audio_path = process_audio_file(audio_path)

    try:
        transcript = speech_to_text(processed_audio_path)
    except Exception as e:
        return jsonify({'error': f'Error in transcription: {str(e)}'}), 400

    extracted_info = call_gpt4_to_extract_info(transcript)

    from models import User
    user_id = User.create_user(extracted_info)
    
    os.remove(audio_path)
    os.remove(processed_audio_path)
    
    return jsonify({
        'transcript': transcript,
        'extracted_info': extracted_info,
        'user_id': str(user_id.inserted_id)
    })

if __name__ == "__main__":
    app.run(debug=True)
