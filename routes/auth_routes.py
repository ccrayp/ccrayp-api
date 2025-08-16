from flask import jsonify, request
from flasgger import swag_from
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from config import Config
from werkzeug.security import check_password_hash

def init_auth_routes(app):
    @app.route('/api/login', methods=['POST'])
    @swag_from('../docs/auth/login.yml')
    def login():
        username = request.json.get('username')
        password = request.json.get('password')
        
        if username != Config.ADMIN_USERNAME or not check_password_hash(Config.ADMIN_PASSWORD_HASH, password):
            return jsonify({"message": "Error. Invalid credentials"}), 401
        
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    @app.route('/api/protected', methods=['GET'])
    @jwt_required()
    @swag_from('../docs/auth/protected.yml')
    def protected():
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user, message="Protected route"), 200