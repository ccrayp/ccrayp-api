from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash


db = SQLAlchemy()
swagger = Swagger()
jwt = JWTManager()


def check_method(current: str, targer: str) -> bool:
    return current.upper() == targer.upper()


def image_url(path: str) -> str:
    return 'https://raw.githubusercontent.com/ccrayp/ccrayp/refs/heads/main/assets/' + path


def json(project) -> dict[str, any]:
    if not project:
        return {}
        
    result = {}
    for key, value in project.__dict__.items():
        if key.startswith('_'):
            continue

        result[key] = value
            
    return result