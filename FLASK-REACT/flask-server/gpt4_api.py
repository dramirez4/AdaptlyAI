import requests
import config

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