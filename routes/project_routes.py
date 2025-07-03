from flasgger import swag_from
from flask import request, jsonify
from flask_jwt_extended import jwt_required

from utilities import check_method, json
from services.project_service import ProjectService

def init_project_routes(app):
    
    @app.route('/api/project/new', methods=['POST'])
    @swag_from('../docs/project/new_project.yml')
    @jwt_required()
    def new_project():
        if not check_method(request.method, 'POST'):
            return jsonify(error='Method not allowed'), 405
        
        data = request.form
        if not data:
            return jsonify(error='No data provided'), 400
        
        required_fields = ['label', 'text', 'img', 'stack', 'link']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'message': f'Error. Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        try:
            project = ProjectService.new_project(data)
            if not project:
                return jsonify(error='Failed to create project'), 500
                               
            return jsonify(id=project.id), 201
        except Exception as e:
            return jsonify(message=f'Internal error. {str(e)}'), 500


    @app.route('/api/project/update/<int:id>', methods=['PUT'])
    @swag_from('../docs/project/update_project_by_id.yml')
    @jwt_required()
    def update_project_by_id(id: int):
        if not check_method(request.method, 'PUT'):
            return jsonify(error='Method not allowed'), 405
        
        data = request.form
        if not data:
            return jsonify(error='No data provided'), 400
        
        required_fields = ['label', 'text', 'img', 'stack', 'link']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'message': f'Error. Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        try:
            ProjectService.update_project_by_id(data, id)
            return jsonify(message='Record was successfully updated'), 200
        
        except Exception as e:
            return jsonify(message=f'Internal error. {str(e)}'), 500



    @app.route('/api/project/list', methods=['GET'])
    @swag_from('../docs/project/get_all_projects.yml')
    # @jwt_required()
    def get_all_projects():
        if not check_method(request.method, 'GET'):
            return jsonify(message='Error. Method not allowed'), 405
        
        try:
            projects = ProjectService.get_all_projects()
            if not projects:
                return jsonify(message='Projects were not found'), 404
            
            return jsonify([json(project) for project in projects]), 200
        
        except Exception as e:
            return jsonify(message=f'Internal error. {str(e)}'), 500


    @app.route('/api/project/<int:id>', methods=['GET'])
    @swag_from('../docs/project/get_project_by_id.yml')
    @jwt_required()
    def get_project_by_id(id: int):
        if not check_method(request.method, 'GET'):
            return jsonify(error='Method not allowed'), 405
        
        if id < 0:
            return jsonify(error='Invalid id', id=id), 400

        try:
            project = ProjectService.get_project_by_id(id)
            
            if not project:
                return jsonify(message='Project with such id does not exist'), 404

            return jsonify(json(project)), 200

        except Exception as e:
            return jsonify(message=f'Internal error. {str(e)}'), 500


    @app.route('/api/project/delete/<int:id>', methods=['DELETE'])
    @swag_from('../docs/project/delete_project_by_id.yml')
    @jwt_required()
    def delete_project_by_id(id: int):
        if not check_method(request.method, 'DELETE'):
            return jsonify(message='Error. Method not allowed'), 405
        
        if id < 0:
            return jsonify(message='Error. Invalid id'), 400

        try:
            project = ProjectService.delete_project_by_id(id)
            if not project:
                return jsonify(message='Project with such id does not exist'), 404
            
            return jsonify(message='Record was successfully deleted'), 200

        except Exception as e:
            return jsonify(message=f'Internal error. {str(e)}'), 500

    
    # @app.route('/api/projects/delete/all', methods=['DELETE'])
    # @swag_from('../docs/project/delete_all_projects.yml')
    # def delete_all_projects():