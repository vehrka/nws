from flask import jsonify
from . import api_1_0_blueprint
from .authentication import auth
from ..models import User


@api_1_0_blueprint.route('/users/')
@auth.login_required
def get_users():
    users = User.query.all()
    return jsonify({'users': [user.to_json() for user in users]})


@api_1_0_blueprint.route('/user/<int:id>')
@auth.login_required
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())
