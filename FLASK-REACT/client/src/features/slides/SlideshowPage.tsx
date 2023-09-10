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
} from "@mantine/core";
import Webcam from "react-webcam";
import { useCallback, useEffect, useRef, useState } from "react";
import showdown from "showdown";
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
  const converter = new showdown.Converter();
  const [slides, setSlides] = useState<{title: string, content?: string}[]>([]);
  // TODO
  const student_info = "computer science student in college with interests in music and art"
  const query = localStorage.getItem("query")
  useEffect(()=>{
    if (slides.length > 0) return;
    fetch(import.meta.env.VITE_PUBLIC_API_URL + "/new-deck", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query,
        student_info
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log({data})
        setSlides(data.map((slide) => ({title: slide})));
      });
  }, [query])

  useEffect(() => {
    if (slides.length > 0 && !slides[currentSlide]?.content) {
      fetch(import.meta.env.VITE_PUBLIC_API_URL + "/gen-slide", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: localStorage.getItem("query"),
          slide_title: slides[currentSlide]?.title,
          slide_titles: slides.map((slide) => slide?.title),
          student_info
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          console.log({data})
          setSlides((slides) => {
            slides[currentSlide].content = data;
            return [...slides];
          });
        });
    }
  }, [currentSlide])

  const confused = useCallback(async (slideIdx: number)=> {
    await fetch(import.meta.env.VITE_PUBLIC_API_URL + "/confused-deck", {body: JSON.stringify({confused_slide_index: slideIdx, query, student_info, deck: slides.map((slide)=>{return slide.title})})})
  }, [query, slides])
  return (
    <AppShell
      padding="md"
      sx={{ minHeight: "100vh" }}
      navbar={
        <Navbar width={{ base: 300 }} p="xs">
          <Title>Slides</Title>
          <List>
            {slides.map((slide, index) => (
              <List.Item
                sx={index === currentSlide ? { backgroundColor: "red" } : {}}
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
          <Title order={1}>AdaptlyAI</Title>
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
      <Link to="/app/query">Back to Query Page</Link>
      <Title order={1}>"{query}"</Title>

      <AspectRatio ratio={16 / 9} px="4rem">
        <Carousel
          getEmblaApi={setEmbla}
          withIndicators
          onSlideChange={(idx) => setCurrentSlide(idx)}
        >
          {slides.map((text, index) => (
            <Carousel.Slide
              sx={(theme) => ({
                backgroundColor:
                  theme.colorScheme === "dark" ? "black" : "white",
                display: "flex",
                flexDirection: "column",
                alignItems: "start",
              })}
              key={index}
            >
              <div
                style={{ display: "contents" }}
                dangerouslySetInnerHTML={{
                  __html: converter.makeHtml(
                    `# ${text?.title}\n\n${text?.content ? text.content : 'Loading...'}`,
                  ),
                }}
              ></div>
            </Carousel.Slide>
          ))}
        </Carousel>
      </AspectRatio>

      {slides.length > 0 && <Text sx={{ textAlign: "center" }}>
        {currentSlide + 1} / {slides.length}
      </Text>}

      <Flex
        align={"center"}
        sx={{ width: "100%", justifyContent: "end" }}
        gap={"sm"}
      >
        <Button onClick={()=>{confused(currentSlide)}}>I'm Confused</Button>
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
