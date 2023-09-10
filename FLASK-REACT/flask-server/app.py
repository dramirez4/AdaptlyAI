import os
import cv2
import numpy as np
from flask import Flask, request, jsonify
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from flask_cors import CORS

app = Flask(__name__)

# Load your pre-trained emotion classification model
model_path = '/Users/davidramirez/Desktop/AdaptlyAI/AdaptlyAI/FLASK-REACT/flask-server/Emotion_Detection/model.h5'  # Update with the correct path
classifier = load_model(model_path)
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Enable CORS for your app
CORS(app)

@app.route("/detect_emotion", methods=["POST"])
def detect_emotion():
    try:
        # Receive the image data from the client
        image_data = request.files['image'].read()

        # Convert the received data into an OpenCV image
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale image
        faces = cv2.CascadeClassifier('/Users/davidramirez/Desktop/AdaptlyAI/AdaptlyAI/FLASK-REACT/flask-server/Emotion_Detection/haarcascade_frontalface_default.xml').detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Check if any faces are detected
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                # Extract the region of interest (ROI) in grayscale
                roi_gray = gray[y:y+h, x:x+w]

                # Resize the ROI to a fixed size (48x48 pixels)
                roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                # Normalize the ROI and prepare it for classification
                roi = roi_gray.astype('float') / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                # Make an emotion prediction using the loaded model
                prediction = classifier.predict(roi)[0]

                # Get the emotion label with the highest confidence
                label = emotion_labels[prediction.argmax()]

                # Return the emotion label as a JSON response
                return jsonify({"emotion": label})

        # If no face is detected in the image, return "No Faces" as a JSON response
        return jsonify({"error": "No Faces"})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
