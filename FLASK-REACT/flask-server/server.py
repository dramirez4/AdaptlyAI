# Import the Flask class from the Flask library
from flask import Flask 
from flask_cors import CORS

# Create an instance of the Flask class and name it 'app'
app = Flask(__name__)
CORS(app)

# Define a route for the '/members' endpoint
@app.route("/members")
def members():
    # Return a JSON response with a list of members
    return {"members": ["Member1", "Member2", "Member3"]}

# This condition ensures that the app is only run if this script is the main program
if __name__ == "__main__":
    # Run the app in debug mode, which provides detailed error messages
    app.run(debug=True)

