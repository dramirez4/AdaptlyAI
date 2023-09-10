import { Text, AspectRatio, Switch, Title, Stack } from "@mantine/core";
import Webcam from "react-webcam";
import { useCallback, useRef, useState, useEffect } from "react";
import axios from "axios";



export function Page1() {
  const [checked, setChecked] = useState(true);
  const webcamRef = useRef<Webcam | null>(null);
  const [emotion, setEmotion] = useState("");
  const capture = useCallback(() => {
    if (webcamRef.current) {
      return webcamRef.current.getScreenshot();
    }
  }, [webcamRef]);

  const detectEmotion = useCallback(async () => {
    try {
      const screenshot = capture();
      if (screenshot) {
        const formData = new FormData();
        const blob = await fetch(screenshot).then((r) => r.blob());
        formData.append("image", blob);

        const response = await axios.post(
          import.meta.env.VITE_PUBLIC_API_URL + "/detect_emotion",
          formData
        );

        const detectedEmotion = response.data.emotion;
        setEmotion(detectedEmotion);
      }
    } catch (error) {
      console.error("Error:", error.message);
      setEmotion("Error: Emotion detection failed");
    }
  }, [capture]);

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
    <Stack align="center" className="background">
      <Title order={1}>Welcome to AdaptlyAI</Title>
      <Text className="title">Home</Text>
      
      <AspectRatio
        ratio={16 / 9}
        sx={{ backgroundColor: "grey", width: "100%" }}
      >
        {checked && <Webcam ref={webcamRef} />}
      </AspectRatio>
      <Switch
        checked={checked}
        onChange={(event) => setChecked(event.currentTarget.checked)}
        label="Use Camera"
      />
      <Text>Detected Emotion: {emotion}</Text>
    </Stack>
  );
}
