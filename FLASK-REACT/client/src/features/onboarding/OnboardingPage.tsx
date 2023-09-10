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
          formData,
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
    let intervalId: number;

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

  const rec = useRef<MediaRecorder | null>(null)
  const chunks = useRef<Blob[]>([])
  useEffect(()=>{
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      console.log("getUserMedia supported.");
      navigator.mediaDevices
        .getUserMedia(
          // constraints - only audio needed for this app
          {
            audio: true,
          },
        )
    
        // Success callback
        .then((stream) => {
          const mediaRecorder = new MediaRecorder(stream);
          console.log({mediaRecorder})
          rec.current = mediaRecorder
          mediaRecorder.ondataavailable = (e) => {
            chunks.current.push(e.data);
          };
  
          mediaRecorder.onstop = async (e) => {
            console.log("recorder stopped");
            const blob = new Blob(chunks.current);
            const formData = new FormData();
            console.log("mime type",rec.current?.mimeType)
            const format = rec.current?.mimeType.split('/')[1].split(';')[0];  // might give 'webm' or 'ogg' or other format based on the browser and MIME type.
            formData.append("file", blob, `audio.${format}`)
            // formData.append("file", blob, "audio.mp3");
  
            const response = await axios.post(
              import.meta.env.VITE_PUBLIC_API_URL + "/speech_to_text",
              formData,
            );
            const info = response.data.extracted_info;
            localStorage.setItem("student_info", JSON.stringify(info));
            alert(Object.values(info))
            window.location.href = "/app/query";
            chunks.current = [];
          };
        })
    
        // Error callback
        .catch((err) => {
          console.error(`The following getUserMedia error occurred: ${err}`);
        });
    } else {
      console.log("getUserMedia not supported on your browser!");
    }
  }, [])

  return (
    <Stack align="center" className="background">
      <Title order={1}>Welcome to AdaptlyAI</Title>
      <Text className="title">Press record and introduce yourself before beginning with the session.</Text>
      <button
        onClick={() => {
          rec.current?.state === 'recording' ? rec.current.stop() : rec.current?.start();
        }}
      >
        {rec.current?.state === 'recording' ? "Stop" : "Record"}
        {rec.current?.state}
      </button>
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
