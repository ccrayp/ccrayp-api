from flasgger import swag_from
from flask import request, jsonify
from flask_jwt_extended import jwt_required

from utilities import check_method, json
from services.post_service import PostService

def init_post_routes(app):
    
    @app.route('/api/post/new', methods=['POST'])
    @jwt_required()
    @swag_from('../docs/posts/new_post.yml')
    def new_post():
        if not check_method(request.method, 'POST'):
            return jsonify(message='Error. Method not allowed'), 405
        
        data = request.form
        if not data:
            return jsonify(message='Error. No data provided'), 400
        
        required_fields = ['label', 'text', 'img', 'link', 'date', 'mode']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'message': f'Error. Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        try:
            post = PostService.new_post(data)
            if not post:
                return jsonify(message='Error. Failed to create post'), 500
                               
            return jsonify(id=post.id), 201
        except Exception as e:
            return jsonify(message=f'Internal error. {str(e)}'), 500


    @app.route('/api/post/update/<int:id>', methods=['PUT'])
    @jwt_required()
    @swag_from('../docs/posts/update_post_by_id.yml')
    def update_post_by_id(id: int):
        if not check_method(request.method, 'PUT'):
            return jsonify(message='Error. Method not allowed'), 405
        
        data = request.form
        if not data:
            return jsonify(message='Error. No data provided'), 400
        
        required_fields = ['label', 'text', 'img', 'link', 'date', 'mode']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'message': f'Error. Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        try:
            PostService.update_post_by_id(data, id)
            return jsonify(message='Record was successfully updated'), 200
        
        except Exception as e:
            return jsonify(message=f'Internal error. {str(e)}'), 500



    @app.route('/api/post/list', methods=['GET'])
    @swag_from('../docs/posts/get_all_posts.yml')
    def get_all_posts():
        if not check_method(request.method, 'GET'):
            return jsonify(message='Error. Method not allowed'), 405
        
        try:
            posts = PostService.get_all_posts()
            if not posts:
                return jsonify(message='Error. Posts were not found'), 404
            
            return jsonify([json(post) for post in posts]), 200
        
        except Exception as e:
            return jsonify(message=f'Internal error. {str(e)}'), 500


    @app.route('/api/post/<int:id>', methods=['GET'])
    @jwt_required()
    @swag_from('../docs/posts/get_post_by_id.yml')
    def get_post_by_id(id: int):
        if not check_method(request.method, 'GET'):
            return jsonify(message='Error. Method not allowed'), 405
        
        if id < 0:
            return jsonify(message='Error. Invalid id', id=id), 400

        try:
            post = PostService.get_post_by_id(id)
            if not post:
                return jsonify(message='Error. Post with such id does not exist'), 404

            return jsonify(json(post)), 200

        except Exception as e:
            return jsonify(message=f'Internal error. {str(e)}'), 500


    @app.route('/api/post/delete/<int:id>', methods=['DELETE'])
    @jwt_required()
    @swag_from('../docs/posts/delete_post_by_id.yml')
    def delete_post_by_id(id: int):
        if not check_method(request.method, 'DELETE'):
            return jsonify(message='Error. Method not allowed'), 405
        
        if id < 0:
            return jsonify(message='Error. Invalid id'), 400

        try:
            post = PostService.delete_post_by_id(id)
            if not post:
                return jsonify(message='post with such id does not exist'), 404
            
            return jsonify(message='Record was successfully deleted'), 200

        except Exception as e:
            return jsonify(message=f'Internal error. {str(e)}'), 500