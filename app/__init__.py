# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as user_auth_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API WITH JWT',
          version='1.0',
          description='Application description')

api.add_namespace(user_ns, path='/user')
api.add_namespace(user_auth_ns, path='/auth')
