from datetime import datetime
from app import mongo

class User:
    collection = mongo.db.users  # 'users' is the name of the collection in MongoDB

    @classmethod
    def create_user(cls, data):
        """Create a new user in the database."""
        user = {
            "experience": data.get("experience"),
            "language": data.get("language"),
            "explanation_style": data.get("explanation_style"),
            "created_at": datetime.utcnow(),
        }
        return cls.collection.insert_one(user)

    @classmethod
    def find_by_id(cls, user_id):
        """Find a user by their unique ID."""
        return cls.collection.find_one({"_id": user_id})
