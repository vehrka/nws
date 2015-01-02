from flask import flash, redirect, render_template, url_for
from flask.ext.login import login_required
from .. import db
from ..models import Game, Player, Side, User, ShpClass, ShpType
from ..decorators import admin_required
from . import admin_blueprint
from .forms import AddClassForm, AddShipForm, AssignSideForm, GameForm, EndGameForm


def populate_players_field(form):
    """Populate the SelectField form the database
    https://github.com/rawrgulmuffins/WTFormMultipleSelectTutorial/blob/master/multiple_select.py"""
    users_choices = [(u.id, u.name) for u in User.query.all()]
    form.players.choices = users_choices


def populate_sides_field(form):
    sides_choices = [(s.id, '{} {}'.format(s.acro, s.desc)) for s in Side.query.all()]
    form.sides.choices = sides_choices


def populate_class_field(form, side=1):
    sclass_choices = [(s.id, '{}, {}'.format(s.acro, s.claoside.acro)) for s in ShpClass.query.filter_by(oside=side).all()]
    oclass_choices = [(s.id, '{}, {}'.format(s.acro, s.claoside.acro)) for s in ShpClass.query.filter(ShpClass.oside != side).all()]
    class_choices = sclass_choices + oclass_choices
    form.shpclass.choices = class_choices


def populate_types_field(form):
    types_choices = [(s.id, '{} {}'.format(s.acro, s.desc)) for s in ShpType.query.all()]
    form.types.choices = types_choices


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


@admin_blueprint.route('/game/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def game(id):
    ogame = Game.query.get(id)
    oplayers = ogame.gameplay.all()
    form = EndGameForm()
    if form.validate_on_submit():
        end = form.endme.data
        if end:
            ogame.finished = True
            db.session.commit()
        flash('The game has been finished')
        return redirect(url_for('.game', id=id))
    sides = {}
    for oplayer in oplayers:
        if oplayer.plasid:
            acro = oplayer.plasid.acro
        else:
            acro = 'Unassigned'
        if acro in sides.keys():
            sides[acro].append(oplayer)
        else:
            sides[acro] = [oplayer]
    return render_template('admin/game.html', form=form,  game=ogame, sides=sides)


@admin_blueprint.route('/sides')
@login_required
@admin_required
def sides():
    return render_template('admin/sides.html')


@admin_blueprint.route('/shptypes')
@login_required
@admin_required
def shptypes():
    return render_template('admin/shptypes.html')


@admin_blueprint.route('/shpclasses', methods=['GET', 'POST'])
@login_required
@admin_required
def shpclasses():
    form = AddClassForm()
    populate_types_field(form)
    populate_sides_field(form)
    sclasses = ShpClass.query.order_by(ShpClass.oside, ShpClass.ctype, ShpClass.acro).all()
    if form.validate_on_submit():
        name = form.name.data
        ctype = form.types.data
        oside = form.sides.data
        acro = form.acro.data
        shpclass = ShpClass(acro=acro, desc=name, oside=oside, ctype=ctype)
        db.session.add(shpclass)
        db.session.commit()
        flash('The class has been added')
        return redirect(url_for('.shpclasses'))
    return render_template('admin/shpclasses.html', sclasses=sclasses, form=form)


@admin_blueprint.route('/player/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def player(id):
    oplayer = Player.query.get(id)
    sideform = AssignSideForm()
    populate_sides_field(sideform)
    addshipform = AddShipForm()
    populate_class_field(addshipform, oplayer.csid)
    if sideform.validate_on_submit():
        side = sideform.sides.data
        oplayer.csid = side
        db.session.commit()
        #if end:
            #ogame.finished = True
            #db.session.commit()
        flash('The side has been asigned')
        return redirect(url_for('.game', id=oplayer.cgam))
    return render_template('admin/player.html', player=oplayer, sideform=sideform, addshipform=addshipform)
