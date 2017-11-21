from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    from .models import Category
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config["development"])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    @app.route('/categories/', methods=['POST', 'GET'])
    def categories():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            if name:
                category = Category(name=name)
                category.save()
                response = jsonify({
                    'id': category.id,
                    'name': category.name,
                    'date_created': category.date_created,
                    'date_modified': category.date_modified
                })
                response.status_code = 201
                return response
        else:
            # GET
            categories = Category.get_all()
            results = []

            for category in categories:
                obj = {
                    'id': category.id,
                    'name': category.name,
                    'date_created': category.date_created,
                    'date_modified': category.date_modified
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response
    
    @app.route('/categories/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def category_manipulation(id, **kwargs):
     # retrieve a category using it's ID
        category = Category.query.filter_by(id=id).first()
        if not category:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            category.delete()
            return {
            "message": "category {} deleted successfully".format(category.id) 
         }, 200

        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            category.name = name
            category.save()
            response = jsonify({
                'id': category.id,
                'name': category.name,
                'date_created': category.date_created,
                'date_modified': category.date_modified
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': category.id,
                'name': category.name,
                'date_created': category.date_created,
                'date_modified': category.date_modified
            })
            response.status_code = 200
            return response
    return app
