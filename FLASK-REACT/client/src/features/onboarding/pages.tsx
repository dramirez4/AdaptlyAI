import { Text, AspectRatio, Switch, Title, Stack, Button } from "@mantine/core";
import Webcam from "react-webcam";
import { useCallback, useRef, useState } from "react";

export function Page1() {
  const [checked, setChecked] = useState(true);
  const webcamRef = useRef<Webcam | null>(null);
  const capture = useCallback(() => {
    if (webcamRef.current) {
      return webcamRef.current.getScreenshot();
    }
  }, [webcamRef]);
  return (
    <Stack align="center">
      <Title order={1}>Welcome to AdaptlyAI</Title>
      <Text>Let's get started.</Text>
      <AspectRatio
        ratio={16 / 9}
        sx={{ backgroundColor: "gray", width: "100%" }}
      >
        {<Webcam ref={webcamRef} />}
      </AspectRatio>
      <Switch
        checked={checked}
        onChange={(event) => setChecked(event.currentTarget.checked)}
        label="Use Camera"
      />
      <Button
        onClick={() => {
          console.log(capture());
        }}
      >
        Take Shot
      </Button>
    </Stack>
  );
}
