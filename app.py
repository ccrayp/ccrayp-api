from config import Config
from flask import Flask, jsonify
from flask_cors import CORS

from routes.auth_routes import init_auth_routes
from routes.home_routes import init_home_routes
from routes.post_routes import init_post_routes
from routes.project_routes import init_project_routes
from routes.technology_routes import init_technology_routes

from utilities import db, swagger, jwt

def init_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    
    db.init_app(app)
    swagger.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()

    init_auth_routes(app)
    init_home_routes(app)
    init_post_routes(app)
    init_project_routes(app)
    init_technology_routes(app)

    @app.errorhandler(404)
    def error():
        return jsonify(message="path wasn't found"), 404

    return app

if __name__ == '__main__':
    app = init_app()
    app.run(port=8000)