import { Carousel } from '@mantine/carousel';
import { AppShell, Navbar, Header, Title, List,Text } from '@mantine/core';

function SlideshowPage() {
  return (
    <AppShell
      padding="md"
      sx={{minHeight: '100vh'}}
      navbar={<Navbar width={{ base: 300 }} p="xs">
        <Title>Slides</Title>
        <List>
            <List.Item>What is a set?</List.Item>
            <List.Item>What is a power set?</List.Item>
            <List.Item>What is a relation?</List.Item>
            <List.Item>What is a function?</List.Item>
            <List.Item>What is a bijection?</List.Item>
            <List.Item>What is a graph?</List.Item>
            <List.Item>What is a tree?</List.Item>
        </List>
      </Navbar>}
      header={<Header height={60} p="xs"><Title order={1}>AdaptlyAI</Title></Header>}
      styles={(theme) => ({
        main: { backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[8] : theme.colors.gray[0] },
      })}
    >
        <Text>Back to Query Page</Text>
        <Title order={1}>Discrete Math</Title>
      <Carousel maw={320} mx="auto" withIndicators height={200}>
      <Carousel.Slide>1</Carousel.Slide>
      <Carousel.Slide>2</Carousel.Slide>
      <Carousel.Slide>3</Carousel.Slide>
      {/* ...other slides */}
    </Carousel>
    </AppShell>
  );
}
export default SlideshowPage