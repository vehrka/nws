from flask import jsonify
from . import api_1_0_blueprint
from ..exceptions import ValidationError


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


def not_allowed(message):
    response = jsonify({'error': 'not allowed', 'message': message})
    response.status_code = 405
    return response


def server_error(message):
    response = jsonify({'error': 'internal server error', 'message': message})
    response.status_code = 500
    return response


@api_1_0_blueprint.errorhandler(ValidationError)
def validation_error(e):
        return bad_request(e.args[0])
