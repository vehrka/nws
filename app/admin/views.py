from flask import render_template
from flask.ext.login import login_required
from ..models import Game
from ..decorators import admin_required
from . import admin_blueprint


#@admin_blueprint.route('/')
#def index():
    #return render_template('index.html')


@admin_blueprint.route('/')
@login_required
@admin_required
def admin():
    return render_template('admin/admin.html')


@admin_blueprint.route('/users')
@login_required
@admin_required
def users():
    return render_template('admin/users.html')


@admin_blueprint.route('/games')
@login_required
@admin_required
def games():
    active_games = Game.query.filter_by(finished=False)
    finished_games = Game.query.filter_by(finished=True)
    return render_template('admin/games.html', active_games=active_games, finished_games=finished_games)


@admin_blueprint.route('/sides')
@login_required
@admin_required
def sides():
    return render_template('admin/sides.html')


@admin_blueprint.route('/players')
@login_required
@admin_required
def players():
    return render_template('admin/players.html')
