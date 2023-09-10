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
  Stack,
} from "@mantine/core";
import Webcam from "react-webcam";
import { useCallback, useRef, useState } from "react";
import showdown from 'showdown'

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
  const converter = new showdown.Converter()
  const slides = [
    {title: "What is a set?", content: "- __TBD__"},
    {title: "What is a power set?", content: "- __TBD__"},
    {title: "What is a relation?", content: "- __TBD__"},
    {title: "What is a function?", content: "- __TBD__"},
    {title: "What is a bijection?", content: "- __TBD__"},
    {title: "What is a graph?", content: "- __TBD__"},
    {title: "What is a tree?", content: "- __TBD__"},
  ];

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
                {slide.title}
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
      <Text>Back to Query Page</Text>
      <Title order={1}>Discrete Math</Title>
      
    <AspectRatio ratio={16 / 9} px="4rem">
        <Carousel
        getEmblaApi={setEmbla}
        withIndicators
        onSlideChange={(idx) => setCurrentSlide(idx)}
        >
        {slides.map((text, index) => (
            <Carousel.Slide sx={(theme) => ({
                
                backgroundColor:
                theme.colorScheme === "dark"
                ? 'black'
                : 'white',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'start'
              })} key={index}>
                <div style={{display:'contents'}} dangerouslySetInnerHTML={{__html:converter.makeHtml(`# ${text.title}\n\n${text.content}`)}}>
                </div>
                </Carousel.Slide>
        ))}
        </Carousel>
    </AspectRatio>
      
          <Text sx={{textAlign: 'center'}}>
          {currentSlide + 1} / {slides.length}
        </Text>

      <Flex
        align={"center"}
        sx={{ width: "100%", justifyContent: "end",  }}
        gap={"sm"}
      >
        <Button>I Understand</Button>
        <Button>I'm Confused</Button>
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
