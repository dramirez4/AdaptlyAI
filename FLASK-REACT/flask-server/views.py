from flask import Blueprint

bp = Blueprint('views', __name__)

@bp.route('/')
def home():
    return "Welcome to the Learning App!"
