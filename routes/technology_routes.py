from flasgger import swag_from
from flask import request, jsonify
from flask_jwt_extended import jwt_required

from utilities import check_method, json
from services.technology_service import TechnologyService

def init_technology_routes(app):
    
    @app.route('/api/technology/new', methods=['POST'])
    @swag_from('../docs/new_technology.yml')
    @jwt_required()
    def new_technology():
        if not check_method(request.method, 'POST'):
            return jsonify(message='Error. Method not allowed'), 405
        
        data = request.form
        if not data:
            return jsonify(message='Error. No data provided'), 400
        
        required_fields = ['label', 'img', 'group', 'mode']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'message': f'Error. Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        try:
            technology = TechnologyService.new_technology(data)
            if not technology:
                return jsonify(message='Error. Failed to create technology'), 500
                               
            return jsonify(id=technology.id), 201
        except Exception as e:
            return jsonify(message=f'Internal error. {str(e)}'), 500


    @app.route('/api/technology/update/<int:id>', methods=['PUT'])
    @swag_from('../docs/technology/update_technology_by_id.yml')
    @jwt_required()
    def update_technology_by_id(id: int):
        if not check_method(request.method, 'PUT'):
            return jsonify(error='Method not allowed'), 405
        
        data = request.form
        if not data:
            return jsonify(error='No data provided'), 400
        
        required_fields = ['label', 'img', 'group', 'mode']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'message': f'Error. Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        try:
            TechnologyService.update_technology_by_id(data, id)
            return jsonify(message='Record was successfully updated'), 200
        
        except Exception as e:
            return jsonify(message=f'Internal error. {str(e)}'), 500



    @app.route('/api/technology/list', methods=['GET'])
    @swag_from('../docs/technology/get_all_technologies.yml')
    # @jwt_required()
    def get_all_technologys():
        if not check_method(request.method, 'GET'):
            return jsonify(message='Error. Method not allowed'), 405
        
        try:
            technologys = TechnologyService.get_all_technologys()
            if not technologys:
                return jsonify(message='Technologies were not found'), 404
            
            return jsonify([json(technology) for technology in technologys]), 200
        
        except Exception as e:
            return jsonify(message=f'Internal error. {str(e)}'), 500


    @app.route('/api/technology/<int:id>', methods=['GET'])
    @swag_from('../docs/technology/get_technology_by_id.yml')
    @jwt_required()
    def get_technology_by_id(id: int):
        if not check_method(request.method, 'GET'):
            return jsonify(message='Error. Method not allowed'), 405
        
        if id < 0:
            return jsonify(message='Error. Invalid id', id=id), 400

        try:
            technology = TechnologyService.get_technology_by_id(id)
            
            if not technology:
                return jsonify(message='Technology with such id does not exist'), 404

            return jsonify(json(technology)), 200

        except Exception as e:
            return jsonify(message=f'Internal error. {str(e)}'), 500


    @app.route('/api/technology/list/<string:group>', methods=['GET'])
    @swag_from('../docs/technology/get_technologies_by_group.yml')
    @jwt_required()
    def get_technologies_by_group(group: str):
        if not check_method(request.method, 'GET'):
            return jsonify(message='Error. Method not allowed'), 405
        
        if id < 0:
            return jsonify(message='Error. Invalid id', id=id), 400

        try:
            technology = TechnologyService.get_technologies_by_group(group)
            
            if not technology:
                return jsonify(message='Technologies with such group does not exist'), 404

            return jsonify(json(technology)), 200

        except Exception as e:
            return jsonify(message=f'Internal error. {str(e)}'), 500


    @app.route('/api/technology/delete/<int:id>', methods=['DELETE'])
    @swag_from('../docs/technology/delete_technology_by_id.yml')
    @jwt_required()
    def delete_technology_by_id(id: int):
        if not check_method(request.method, 'DELETE'):
            return jsonify(message='Error. Method not allowed'), 405
        
        if id < 0:
            return jsonify(message='Error. Invalid id'), 400

        try:
            technology = TechnologyService.delete_technology_by_id(id)
            if not technology:
                return jsonify(message='Technology with such id does not exist'), 404
            
            return jsonify(message='Record was successfully deleted'), 200

        except Exception as e:
            return jsonify(message=f'Internal error. {str(e)}'), 500

    
    # @app.route('/api/technologys/delete/all', methods=['DELETE'])
    # @swag_from('../docs/technology/delete_all_technologys.yml')
    # def delete_all_technologys():