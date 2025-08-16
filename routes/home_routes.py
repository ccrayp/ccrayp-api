from flask import request, redirect, jsonify, render_template
from flasgger import swag_from

def init_home_routes(app):
    @app.route('/', methods=['GET'])
    def root():
        if request.method != 'GET':
            return jsonify({
                'status': 'error',
                'message': 'incorrect method <' + request.method + '>'
            }), 404
        
        return render_template('index.html')