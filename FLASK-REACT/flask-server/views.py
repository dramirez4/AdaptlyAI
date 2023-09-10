# This file will contain our Flask route handlers (views) related to database operations. 
from flask import request, jsonify
from app import app
from models import User

@app.route('/onboard', methods=['POST'])
def onboard_user():
    data = request.get_json()
    user_id = User.create_user(data)
    return jsonify({"message": "User onboarded successfully", "user_id": str(user_id.inserted_id)}), 201
