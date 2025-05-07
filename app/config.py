import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///candidates.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False