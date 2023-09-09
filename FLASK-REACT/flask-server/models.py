from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    experience_summary = db.Column(db.String(500))
    language = db.Column(db.String(100))
    learning_style = db.Column(db.String(500))