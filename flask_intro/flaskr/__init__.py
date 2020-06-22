from flask import Flask, jsonify
import os
from models import setup_db,Plant
from flask_cors import CORS


# we will use only the basic config for now

def create_app(test_config=None):
    app= Flask(__name__, instance_relative_config=True)
    # CORS(app)
    cors= CORS(app, resources={r"*/api/*", {"origins":"*"}})
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    #     )
    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass
    @app.after_request
    def after_request(response):
        response.header.add({'Access-Control-Allow-Headers','Content-Type, Authorization'})
        response.header.add({'Access-Control-Allow-Methods','GET, POST, PATCH, DELETE, OPTIONS'})    
    
    @app.route('/')
    @cross_origin       #decorator just for allowing cors just for this end points
    def new_func():
        return jsonify({"hello":"world"})
    
    @app.route('/')
    
    
    return app