import os
import requests
import config
import openai
import re
import elevenlabs
from elevenlabs import set_api_key
set_api_key(config.ELEVEN_KEY)

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
        {"role": "user", "content": f"The person mentioned: '{transcript}'. Extract a hobby or personal experience they might have talked about and write one sentence of that so that we can use that for creating analogies in the future."}
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
    return f'You are an expert educator. You are slightly witty, funny.  Help your student learn new materials by creating engaging and accessible slideshows that cater to their learning style and background while provide intuitive explanations. Start your learning session by using analogies and other learning devices that best fit their needs based on the following information about the student saying that you got this info about them based on what they said here: """{student_info}"""'

def NEW_DECK_PROMPT_TEMPLATE(query: str):
    return f'Given this """{query}""" return a newline-delimited-list of slide titles that you would include in a slideshow used to teach me about """{query}""". Do not generate the content associated with the slides until asked. Do not include any text other than the requested content. '

def CONFUSED_PROMPT_TEMPLATE(confused_slide_title: str):
    return f'I was confused by this slide: """{confused_slide_title}""". Return an amended new-line-delimited list of slide titles, and include at least 1, but no more than 3, new slides that you would add to the slide deck, breaking down the given slide\'s topic into simpler parts until it\'s at just the right level for me to gain an understanding and help me resolve my doubts.'

def GEN_SLIDE_PROMPT_TEMPLATE(query: str, slide_title: str):
    return f'"I want to learn about """{query}""", currently on the slide """{slide_title}""". Create the content of this slide. Be concise and clear with your explanations. Do not exceed 1000 characters per slide. Feel free to address me by name and mention other information that I gave you about me. Do not include any text other than the requested content. Do not unnecessarily repeat content that will be covered on other slides within the deck. Be sure to keep previously given information about me in mind.'

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

# def make_new_slide(student_info: str, query: str, slide_title: str, slide_titles: list[str]):
#     out = ""
#     out2 = ""
#     out3 = ""
#     fname = "" 
#     try:    
#         response = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=make_new_slide_prompt(student_info, query, slide_title, slide_titles)
#         )
#         out = res_str(response)
#         print(response)
#     except Exception as e:
#         print(e)

#     try:
#         response2 = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[{'role':'user', 'content': f'Use up to 3 short, concise bullet points to summarize the following content for use in a simple slideshow. Remove any special, non-punctuation characters: """{out}"""'}]
#         )
#         out2 = res_str(response2)
#         print(response2)
#     except Exception as e:
#         print(e)
    
#     try:
#         response3 = openai.ChatCompletion.create(
#             model="gpt-4",
#             messages=[{'role':'user', 'content': f'Select an item that can be illustrated to add more emphasis to the following point: """{out2}"""'}]
#         )
#         out3 = res_str(response3)
#         print(response3)
#     except Exception as e:
#         print(e)
    
#     try:
#         voice = elevenlabs.Voice.from_id("VR6AewLTigWG4xSOukaG")
#         voice.settings.similarity_boost = 0.89
#         voice.settings.stability = 0.09
#         voice.settings.style = 0
#         voice.settings.use_speaker_boost = True
#         CHUNK = 1024
#         audio = elevenlabs.generate(text=out, voice=voice, stream_chunk_size=CHUNK, stream=True)
#         from uuid import uuid4
#         file_id = str(uuid4())
#         fname= f"static/{file_id}.mp3"
#         # with open (fname, "wb") as f:
#         #     f.write(audio)
#         with open(fname, 'wb') as f:
#             for chunk in audio:
#                 if chunk:
#                     f.write(chunk)
#     except Exception as e:
#         print(e)
#     return out2, 'http://localhost:5000/' + fname, out3 

import os
from google.cloud import texttospeech

def make_new_slide(student_info: str, query: str, slide_title: str, slide_titles: list[str]):
    out = ""
    out2 = ""
    out3 = ""
    fname = "" 
    try:    
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=make_new_slide_prompt(student_info, query, slide_title, slide_titles)
        )
        out = res_str(response)
        print(response)
    except Exception as e:
        print(e)

    try:
        response2 = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{'role':'user', 'content': f'Use up to 3 short, concise bullet points to summarize the following content for use in a simple slideshow. Remove any special, non-punctuation characters: """{out}"""'}]
        )
        out2 = res_str(response2)
        print(response2)
    except Exception as e:
        print(e)
    
    try:
        response3 = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{'role':'user', 'content': f'Select an item that can be illustrated to add more emphasis to the following point: """{out2}"""'}]
        )
        out3 = res_str(response3)
        print(response3)
    except Exception as e:
        print(e)
    
    try:
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=out)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        from uuid import uuid4
        file_id = str(uuid4())
        fname= f"static/{file_id}.mp3"
        with open(fname, "wb") as out:
            out.write(response.audio_content)
    except Exception as e:
        print(e)
    return out2, 'http://localhost:5000/' + fname, out3 
    




def make_confused_deck(student_info: str, query: str, confused_slide_title: str, slide_titles: list[str]):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            *make_new_deck_prompt(student_info, query),
            {"role": "assistant", "content": "\n".join(slide_titles)},
            {"role": "user", "content": CONFUSED_PROMPT_TEMPLATE(confused_slide_title)},
        ]
    )
    print(response)
    return deck_res_to_list(response)
