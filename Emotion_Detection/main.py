# Import necessary libraries
from keras.models import load_model  # Load a pre-trained machine learning model
from time import sleep  # Import a function to introduce delays
from keras.preprocessing.image import img_to_array  # Convert images to arrays
from keras.preprocessing import image  # Image preprocessing tools
import cv2  # OpenCV library for computer vision tasks
import numpy as np  # Library for numerical operations

# Initialize a face classifier using a pre-trained XML file
face_classifier = cv2.CascadeClassifier(
    r'/Users/davidramirez/Desktop/AdaptlyAI/Emotion_Detection/haarcascade_frontalface_default.xml')

# Load a pre-trained emotion classification model
classifier = load_model(
    r'/Users/davidramirez/Desktop/AdaptlyAI/Emotion_Detection/model.h5')

# Define a list of emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear',
                  'Happy', 'Neutral', 'Sad', 'Surprise']

# Open a video capture device (usually the webcam, indicated by 0)
cap = cv2.VideoCapture(0)

# Start an infinite loop for video processing
while True:
    # Read a frame from the video capture device
    _, frame = cap.read()

    # Check if the frame is empty (no image received)
    if frame is None:
        continue

    # Initialize an empty list to store emotion labels
    labels = []

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_classifier.detectMultiScale(gray)

    # Loop through the detected faces
    for (x, y, w, h) in faces:
        # Draw a rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)

        # Extract the region of interest (ROI) in grayscale
        roi_gray = gray[y:y+h, x:x+w]

        # Resize the ROI to a fixed size (48x48 pixels)
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

        # Check if the ROI is not empty
        if np.sum([roi_gray]) != 0:
            # Normalize the ROI and prepare it for classification
            roi = roi_gray.astype('float') / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            # Make an emotion prediction using the loaded model
            prediction = classifier.predict(roi)[0]

            # Get the emotion label with the highest confidence
            label = emotion_labels[prediction.argmax()]

            # Define the position to display the emotion label
            label_position = (x, y)

            # Add the emotion label to the frame
            cv2.putText(frame, label, label_position,
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            # If no face is detected in the ROI, display "No Faces"
            cv2.putText(frame, 'No Faces', (30, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame with emotion labels
    cv2.imshow('Emotion Detector', frame)

    # Check for a key press ('q' key to exit the loop)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture device
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()

