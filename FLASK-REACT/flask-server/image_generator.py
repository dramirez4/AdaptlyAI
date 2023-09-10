from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key here
api_key = "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"

# Initialize the OpenAI API client
openai.api_key = api_key

@app.route('/generate_image', methods=['GET'])
def generate_image():
    # Define a text prompt describing the image you want
    prompt = "Generate an image of a blue cat with wings sitting on a cloud."

    # Make an API call to generate the image
    response = openai.Image.create(
        model="image-alpha-001",  # Choose an appropriate DALL·E model
        prompt=prompt,
        n=1,  # Number of images to generate (you can adjust this)
        size="256x256"  # Specify the image size (you can adjust this)
    )

    # Get the URL of the generated image
    image_url = response.data[0]["url"]

    return jsonify({'imageURL': image_url})

if __name__ == '__main__':
    app.run(debug=True)

