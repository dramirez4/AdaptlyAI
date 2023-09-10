import requests
import config
import openai

def call_gpt4_to_extract_info(transcript):
    ENDPOINT = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {config.OPENAI_API_KEY}",
    }

    def make_api_call(messages):
        data = {
            "model": "gpt-4",   # Specify the model, adjust if necessary
            "messages": messages
        }
        response = requests.post(ENDPOINT, headers=headers, json=data)
        response_data = response.json()
        
        # Log the full API response for debugging
        print(response_data)

        if 'choices' in response_data:
            return response_data['choices'][0]['message']['content'].strip()
        else:
            print(f"Unexpected API response for messages: {messages}")
            return "Error extracting data"
    
    # Extract hobbies or experiences for analogies
    messages_experience = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"The person mentioned: '{transcript}'. Extract a hobby or personal experience they might have talked about and write one sentence of that so that we can use that for creating anlogies in the future."}
    ]
    experience_summary = make_api_call(messages_experience)

    # Extract preferred explanation style
    messages_style = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"The person mentioned: '{transcript}'. Identify their preferred explanation style and return in one concise sentence."}
    ]
    style_summary = make_api_call(messages_style)

    # Extract preferred language
    messages_language = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"The person mentioned: '{transcript}'. Determine their preferred language for learning and return language in one word"}
    ]
    language_summary = make_api_call(messages_language)

    return {
        "experience": experience_summary,
        "style": style_summary,
        "language": language_summary
    }


def PROMPT_BASE_TEMPLATE(student_info: str):
    return f'You are an expert educator. Help your student learn new materials by creating engaging and accessible slideshows that cater to their learning style and background. Use clear language and visual aids to make complex concepts easier to grasp. Use analogies and other learning devices that best fit their needs based on the following information about the student: """{student_info}"""'

def NEW_DECK_PROMPT_TEMPLATE(query: str):
    return f'I will be learning about """{query}""". Return a newline-delimited-list of slide titles that you would include in a slideshow used to teach me about """{query}""". Do not generate the content associated with the slides until asked.'

def CONFUSED_PROMPT_TEMPLATE(confused_slide_title: str):
    return f'I was confused by this slide: """{confused_slide_title}""". Return an amended new-line-delimited list of slide titles, and include at least 1, but no more than 3, new slides that you would add to the slide deck, breaking down the given slide\'s topic into simpler parts until it\'s at just the right level for me to gain an understanding and help me resolve my doubts.'

def GEN_SLIDE_PROMPT_TEMPLATE(query: str, slide_title: str):
    return f'"I\'m learning about """{query}""", currently on the slide """{slide_title}""". Create the content of this slide. Utilize Markdown for rich text formatting. Do not generate any images or image URLs. Do not be overly verbose. Do not unnecessarily repeat content that will be covered on other slides within the deck. Be sure to keep previously given information about me in mind.'

def make_new_deck_prompt(student_info: str, query: str):
    return [{"role": "system", "content": PROMPT_BASE_TEMPLATE(student_info)},
    {"role": "user", "content": NEW_DECK_PROMPT_TEMPLATE(query)}]

def make_new_deck(student_info: str, query: str):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=make_new_deck_prompt(student_info, query)
        
    )
    print(response)
    return deck_res_to_list(response)

def deck_res_to_list(res):
    return res_str(res).split('\n')

def res_str(res):
    return res['choices'][0]['message']['content']

def make_new_slide_prompt(student_info: str, query: str, slide_title: str, slide_titles: list[str]):
    return [{"role": "system", "content": PROMPT_BASE_TEMPLATE(student_info)},
    {"role": "assistant", "content": "\n".join(slide_titles)},
    {"role": "user", "content": GEN_SLIDE_PROMPT_TEMPLATE(query, slide_title)}]

def make_new_slide(student_info: str, query: str, slide_title: str, slide_titles: list[str]):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=make_new_slide_prompt(student_info, query, slide_title, slide_titles)
        
    )
    print(response)
    return res_str(response)

def make_confused_deck(student_info: str, query: str, confused_slide_title: str, slide_titles: list[str]):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            *make_new_deck_prompt(student_info, query),
            {"role": "assistant", "content": "\n".join(slide_titles)},
            {"role": "user", "content": CONFUSED_PROMPT_TEMPLATE(confused_slide_title)},
        ]
    )
    print(response)
    return deck_res_to_list(response)
