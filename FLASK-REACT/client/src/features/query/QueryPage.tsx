import { TextInput, Group, Button } from "@mantine/core";
import { useForm } from "@mantine/form";

const QueryPage = () => {
  const form = useForm({
    initialValues: {
      query: '',
    },

    validate: {
      query: (value) => (value.length > 0 ? null : 'Invalid query'),
    },
  });
    return (
      <div>
        <form onSubmit={form.onSubmit((values) => console.log(values))}>
          <TextInput
          variant="filled"
          placeholder="I want to learn about..."
            withAsterisk
            label="Query"
            {...form.getInputProps('query')}
          />

          <Group position="right" mt="md">
            <Button type="submit">Submit</Button>
          </Group>
        </form>
      </div>
    )
}

export default QueryPage