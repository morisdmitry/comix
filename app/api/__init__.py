from flask import Blueprint
from flask_restx import Api


api = Api(version='1.0', title='Comix API', description='comix api', validate=True)
api_blueprint = Blueprint('/api', __name__, url_prefix='/api')

from app.api.routes import *