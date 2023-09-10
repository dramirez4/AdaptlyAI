import requests
import config

def call_gpt4_to_extract_info(transcript):
    ENDPOINT = "https://api.openai.com/v1/engines/davinci-codex/completions"

    # Extract hobbies or experiences for analogies
    prompt_experience = f"The person mentioned: '{transcript}'. Extract a hobby or personal experience they might have talked about."

    # Extract preferred explanation style
    prompt_style = f"The person mentioned: '{transcript}'. Identify their preferred explanation style."

    # Extract preferred language
    prompt_language = f"The person mentioned: '{transcript}'. Determine their preferred language for learning."

    headers = {
        "Authorization": f"Bearer {config.OPENAI_API_KEY}",
    }
    data_experience = {
        "prompt": prompt_experience,
        "max_tokens": 50  
    }

    response_experience = requests.post(ENDPOINT, headers=headers, json=data_experience)
    experience_summary = response_experience.json()['choices'][0]['text'].strip()

    # API call for 'prompt_style' 
    data_style = {
        "prompt": prompt_style,
        "max_tokens": 50  
    }

    response_style = requests.post(ENDPOINT, headers=headers, json=data_style)
    style_summary = response_style.json()['choices'][0]['text'].strip()

    # API call for 'prompt_language' 
    data_language = {
        "prompt": prompt_language,
        "max_tokens": 50  
    }

    response_language = requests.post(ENDPOINT, headers=headers, json=data_language)
    language_summary = response_language.json()['choices'][0]['text'].strip()

    return {
        "experience": experience_summary,
        "style": style_summary,
        "language": language_summary
    }
