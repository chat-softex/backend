# middlewares/cors_middleware.py:
from flask_cors import CORS

def init_cors(app):
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
