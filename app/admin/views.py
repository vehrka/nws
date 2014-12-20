from flask import flash, redirect, render_template, url_for
from flask.ext.login import login_required
from .. import db
from ..models import Game, Player, User
from ..decorators import admin_required
from . import admin_blueprint
from .forms import GameForm


def populate_players_field(form):
    """Populate the SelectField form the database
    https://github.com/rawrgulmuffins/WTFormMultipleSelectTutorial/blob/master/multiple_select.py"""
    users_choices = [(u.id, u.name) for u in User.query.all()]
    form.players.choices = users_choices


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
    populate_players_field(form)
    if form.validate_on_submit():
        name = form.name.data
        desc = form.desc.data
        players = form.players.data
        game = Game(name=name, desc=desc)
        db.session.add(game)
        db.session.commit()
        for player in players:
            db.session.add(Player(cuse=player, cgam=game.id))
        db.session.commit()
        flash('The game has been added')
        return redirect(url_for('.games'))
    active_games = Game.query.filter_by(finished=False).all()
    finished_games = Game.query.filter_by(finished=True).all()
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
