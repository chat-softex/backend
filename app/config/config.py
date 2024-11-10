# app/config/config.py:
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    FIREBASE_CONFIG = os.getenv('FIREBASE_CONFIG')
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
    DEBUG = os.getenv('FLASK_ENV') == 'development'