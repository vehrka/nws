from flask import render_template
from flask.ext.login import login_required
from app.decorators import admin_required
from . import admin_blueprint


@admin_blueprint.route('/')
def index():
    return render_template('index.html')


@admin_blueprint.route('/admin')
@login_required
@admin_required
def admin():
    return render_template('admin/admin.html')


@admin_blueprint.route('/admin/users')
@login_required
@admin_required
def users():
    return render_template('admin/users.html')


@admin_blueprint.route('/admin/games')
@login_required
@admin_required
def games():
    return render_template('admin/games.html')


@admin_blueprint.route('/admin/sides')
@login_required
@admin_required
def sides():
    return render_template('admin/sides.html')


@admin_blueprint.route('/admin/players')
@login_required
@admin_required
def players():
    return render_template('admin/players.html')
