from datetime import timedelta
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
    ADMIN_PASSWORD_HASH = generate_password_hash(os.getenv('ADMIN_PASSWORD'))

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)
    JWT_TOKEN_LOCATION = ['cookies', 'headers']