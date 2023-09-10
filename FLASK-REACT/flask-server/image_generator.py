from flask import Blueprint, request, jsonify
import openai

bp = Blueprint('img', __name__)

# Load OpenAI API key from environment variable
# api_key = os.getenv("OPENAI_API_KEY", "YOUR_DEFAULT_API_KEY_HERE")
# openai.api_key = api_key

@bp.route('/generate_image', methods=['POST'])
def generate_image():
    data = request.get_json()

    # Check if prompt is provided
    if not data or 'prompt' not in data:
        return jsonify({'error': 'No prompt provided'}), 400

    prompt = data['prompt']

    try:
        # Make an API call to generate the image
        response = openai.Image.create(
            model="image-alpha-001",  # Choose an appropriate DALL·E model
            prompt=prompt,
            n=1,  # Number of images to generate
            size="256x256"  # Image size
        )

        # Check for a valid response from OpenAI
        if 'data' in response and response['data']:
            image_url = response['data'][0]["url"]
            return jsonify({'imageURL': image_url})
        else:
            return jsonify({'error': 'Failed to generate image'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

"""
How to use:

When you call the endpoint /generate_image through a POST request, include a JSON object with a prompt key, e.g.,

json
Copy code
{
  "prompt": "Generate an image of a blue cat with wings sitting on a cloud."
}
The response will include the URL to the generated image or an error message.

Remember to set the environment variable OPENAI_API_KEY with your OpenAI API key before running the Flask application. Using environment variables for storing secrets is a more secure practice than hardcoding them.
"""