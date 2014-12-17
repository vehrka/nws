from flask import Blueprint

api_1_0_blueprint = Blueprint('api', __name__)

from . import authentication, users, errors
