import React, { useCallback, useEffect, useRef, useState } from "react";
import axios from "axios";
import Webcam from "react-webcam";
import './home.css';

export function Page1() {
  const [checked, setChecked] = useState(true);
  const [emotion, setEmotion] = useState("");
  const [imageURL, setImageURL] = useState(""); // State to store the image URL
  const webcamRef = useRef<Webcam | null>(null);

  const capture = useCallback(() => {
    if (webcamRef.current) {
      return webcamRef.current.getScreenshot();
    }
    return null;
  }, [webcamRef]);

  const detectEmotion = async () => {
    try {
      const screenshot = capture();
      if (screenshot) {
        const formData = new FormData();
        const blob = await fetch(screenshot).then((r) => r.blob());
        formData.append("image", blob);

        const response = await axios.post(
          "http://127.0.0.1:5000/detect_emotion",
          formData
        );

        const detectedEmotion = response.data.emotion;
        setEmotion(detectedEmotion);

        // Set the image URL received from the server
        setImageURL(response.data.imageURL);
      }
    } catch (error) {
      console.error("Error:", error.message);
      setEmotion("Error: Emotion detection failed");
    }
  };

  useEffect(() => {
    let intervalId: NodeJS.Timeout;

    if (checked) {
      // Start capturing and detecting emotion every 0.5 seconds
      intervalId = setInterval(detectEmotion, 500);
    } else {
      // Clear the interval if not using the camera
      clearInterval(intervalId);
    }

    return () => {
      // Cleanup the interval when the component unmounts
      clearInterval(intervalId);
    };
  }, [checked, detectEmotion]);

  return (
    <div className="page-container">
      <h1>Welcome to AdaptlyAI</h1>
      <p>Let's get started.</p>
      <div className={`camera-container ${checked ? "active" : ""}`}>
        {checked && <Webcam ref={webcamRef} className="webcam" />}
      </div>
      <label>
        Use Camera
        <input
          type="checkbox"
          checked={checked}
          onChange={(event) => setChecked(event.target.checked)}
        />
      </label>
      <div>
        <p>Detected Emotion: {emotion}</p>
        {imageURL && <img src={imageURL} alt="Generated Image" />}
      </div>
    </div>
  );
}




