from flask import flash, redirect, render_template, url_for
from flask.ext.login import login_required
from ..models import Game
from ..decorators import admin_required
from . import admin_blueprint
from .forms import GameForm


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


@admin_blueprint.route('/games', methods=['GET', 'POST'])
@login_required
@admin_required
def games():
    form = GameForm()
    if form.validate_on_submit():
        flash('The game has been added')
        return redirect(url_for('.games'))
    active_games = Game.query.filter_by(finished=False)
    finished_games = Game.query.filter_by(finished=True)
    return render_template('admin/games.html', form=form, active_games=active_games, finished_games=finished_games)


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
