import { Carousel, Embla } from "@mantine/carousel";
import {
  AppShell,
  Navbar,
  Header,
  Title,
  List,
  Text,
  AspectRatio,
  Flex,
  Button,
  Loader,
  Stack,
} from "@mantine/core";
import Webcam from "react-webcam";
import { useCallback, useEffect, useRef, useState } from "react";
import { Link } from "@tanstack/react-router";

function SlideshowPage() {
  const webcamRef = useRef<Webcam | null>(null);
  const [embla, setEmbla] = useState<Embla | null>(null);

  const switchSlide = useCallback(
    (index: number) => {
      embla?.scrollTo(index, true);
    },
    [embla],
  );

  const [currentSlide, setCurrentSlide] = useState(0);
  const [slides, setSlides] = useState<{ title: string; content?: string, audio_url?: string, img_prompt?: string }[]>(
    [],
  );
  const student_info = localStorage.getItem("student_info");
  const query = localStorage.getItem("query");
  useEffect(() => {
    if (slides.length > 0) return;
    fetch(import.meta.env.VITE_PUBLIC_API_URL + "/new-deck", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query,
        student_info,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log({ data });
        setSlides(data.map((slide) => ({ title: slide })));
        genSlide(currentSlide)
      });
  }, [query]);

  const genSlide = useCallback((s)=>{
    const slideTitle = slides[s]?.title;
    if (!slideTitle) return; // Guard clause to ensure slide title is defined
    
    fetch(import.meta.env.VITE_PUBLIC_API_URL + "/gen-slide", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: localStorage.getItem("query"),
        slide_title: slides[s]?.title,
        slide_titles: slides.map((slide) => slide?.title),
        student_info,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log({ data });
        setSlides((slides) => {
          slides[s].content = data[0];
          slides[s].audio_url = data[1];
          slides[s].img_prompt = data[2];
          return [...slides];
        });
      });
  }, [slides])
  // useEffect(() => {
  //   if (slides.length > 0 && !slides[currentSlide]?.content) {
  //     genSlide(currentSlide)
  //   }
  // }, [slides, currentSlide]);
  useEffect(() => {
    if (slides.length > 0 && slides[currentSlide] && !slides[currentSlide].content) {
      genSlide(currentSlide);
    }
  }, [slides, currentSlide, genSlide]);
  

  const confused = useCallback(
    async (slideIdx: number) => {
      await fetch(import.meta.env.VITE_PUBLIC_API_URL + "/confused-deck", {
        body: JSON.stringify({
          confused_slide_index: slideIdx,
          query,
          student_info,
          deck: slides.map((slide) => {
            return slide.title;
          }),
        }),
      });
    },
    [query, slides],

    );
    const audioEls = useRef<Record<number, HTMLAudioElement | null>>({})
  return (
    <AppShell
      padding="md"
      sx={{ minHeight: "100vh" }}
      navbar={
        <Navbar width={{ base: 300 }} p="xs">
          <Title>Slides</Title>
          {slides.length == 0 && <Loader sx={{margin:"4rem"}} />}
          <List>
            {slides.map((slide, index) => (
              <List.Item
                sx={index === currentSlide ? { fontWeight: "bold" } : {}}
                key={index}
                onClick={() => switchSlide(index)}
              >
                {slide?.title}
              </List.Item>
            ))}
          </List>
        </Navbar>
      }
      header={
        <Header height={60} p="xs">
          <Title order={1}><Link to="/app/onboarding">AdaptlyAI</Link></Title>
        </Header>
      }
      styles={(theme) => ({
        main: {
          backgroundColor:
            theme.colorScheme === "dark"
              ? theme.colors.dark[8]
              : theme.colors.gray[0],
        },
      })}
    >
      <Stack>
      <Link to="/app/query"><Text>Back to Query Page</Text></Link>
      <Title order={1}>{query}</Title>
        <Carousel
        px="4rem"
          getEmblaApi={setEmbla}
          withIndicators
          onSlideChange={(idx) => {
            setCurrentSlide(idx)
            if (audioEls.current[idx]) audioEls.current[idx]?.play()
          }}
        >
          {slides.map((text, index) => (
            <Carousel.Slide
              sx={(theme) => ({
                backgroundColor:
                  theme.colorScheme === "dark" ? "black" : "white",
                display: "flex",
                flexDirection: "column",
                alignItems: "start",
                height: '60vh', 
                overflow: 'scroll'
              })}
              key={index}
            >
              {slides[index]?.audio_url && (
                <audio ref={(r) => audioEls.current[index] = r} onEnded={() => switchSlide(index + 1)}
                  controls
                  autoPlay={index === 0}
                  src={slides[index]?.audio_url}
                ></audio>
              )}
              {!!slides[index].img_prompt && (
                <DalleImage prompt={slides[index].img_prompt!} />
              )}
              {slides.length == 0 || !text.content && <Loader sx={{margin:"4rem"}} />}
              <Title>{text?.title}</Title>
              <Text>{text.content}</Text>
            </Carousel.Slide>
          ))}
        </Carousel>
</Stack>

      {slides.length > 0 && (
        <Text sx={{ textAlign: "center" }}>
          {currentSlide + 1} / {slides.length}
        </Text>
      )}

      <Flex
        align={"center"}
        sx={{ width: "100%", justifyContent: "end" }}
        gap={"sm"}
      >
        <Button
          onClick={() => {
            confused(currentSlide);
          }}
        >
          I'm Confused
        </Button>
        <AspectRatio
          ratio={1 / 1}
          sx={{
            backgroundColor: "gray",
            width: "6rem",
            borderRadius: "999px",
            overflow: "hidden",
          }}
        >
          <Webcam ref={webcamRef} />
        </AspectRatio>
      </Flex>
    </AppShell>
  );
}
export default SlideshowPage;

const DalleImage = ({ prompt }: { prompt: string }) => {
  const [img, setImg] = useState<string | null>(null);
  useEffect(() => {
    if (img) return
    fetch(import.meta.env.VITE_PUBLIC_API_URL + "/generate_image", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        prompt,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log({ data });
        setImg(data['imageURL']);
      });
  }, [prompt]);
  return (
    <img
      src={img ? img : ""}
      style={{ width: "100%", height: "100%" }}
    />
  );
}
