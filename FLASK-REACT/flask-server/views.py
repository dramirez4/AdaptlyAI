
# This file will contain our Flask route handlers (views) related to database operations. 
from flask import Blueprint, request, jsonify

bp = Blueprint('views', __name__)
@bp.route('/onboard', methods=['POST'])
def onboard_user():
    from models import User
    data = request.get_json()
    user_id = User.create_user(data)
    return jsonify({"message": "User onboarded successfully", "user_id": str(user_id.inserted_id)}), 201