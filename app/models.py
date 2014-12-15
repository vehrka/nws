# coding: utf-8
from . import db, login_manager
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Approle(db.Model):
    __tablename__ = 'a_approle'

    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(100))

    roluser = db.relationship('RArousr', backref='a_approle')

    def __repr__(self):
        return '<Rol {}>'.format(self.desc)


class Side(db.Model):
    __tablename__ = 'a_sides'

    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(75))

    sideplay = db.relationship('Player', backref='a_sides')

    def __repr__(self):
        return '<Side {}>'.format(self.desc)


class RArousr(db.Model):
    __tablename__ = 'r_arousr'

    id = db.Column(db.Integer, primary_key=True)
    capr = db.Column(db.Integer, db.ForeignKey('a_approle.id'))
    cuse = db.Column(db.Integer, db.ForeignKey('t_users.id'))


class ShpClass(db.Model):
    __tablename__ = 't_shpclasses'

    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(100))

    clacoun = db.relationship('Counter', backref='t_shpclasses')
    clahcoun = db.relationship('HCounter', backref='t_shpclasses')

    def __repr__(self):
        return '<Counter Class {}>'.format(self.desc)


class Counter(db.Model):
    __tablename__ = 't_counters'

    id = db.Column(db.Integer, primary_key=True)
    cclas = db.Column(db.Integer, db.ForeignKey('t_shpclasses.id'))
    name = db.Column(db.String(100))
    bearing = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    height = db.Column(db.Integer)
    detected = db.Column(db.Boolean)
    lat = db.Column(db.Integer)
    lon = db.Column(db.Integer)

    counform = db.relationship('Formation', backref='t_formations')
    counhist = db.relationship('HCounter', backref='t_h_counter')

    def __repr__(self):
        return '<Counter {}>'.format(self.name)


class Formation(db.Model):
    __tablename__ = 't_formations'

    id = db.Column(db.Integer, primary_key=True)
    cplay = db.Column(db.Integer, db.ForeignKey('t_players.id'))
    ccou = db.Column(db.Integer, db.ForeignKey('t_counters.id'))


class Game(db.Model):
    __tablename__ = 't_games'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    desc = db.Column(db.Text)
    date = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))
    finished = db.Column(db.Boolean)

    gameplay = db.relationship('Player', backref='t_games')
    gameturn = db.relationship('Turn', backref='t_games')

    def __repr__(self):
        return '<Game {}>'.format(self.name)


class HCounter(db.Model):
    __tablename__ = 't_h_counter'

    id = db.Column(db.Integer, primary_key=True)
    cclas = db.Column(db.Integer, db.ForeignKey('t_shpclasses.id'))
    ccou = db.Column(db.Integer, db.ForeignKey('t_counters.id'))
    name = db.Column(db.String(100))
    bearing = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    height = db.Column(db.Integer)
    detected = db.Column(db.Boolean)
    cturn = db.Column(db.Integer, db.ForeignKey('t_turns.id'))
    lat = db.Column(db.Integer)
    lon = db.Column(db.Integer)


class Player(db.Model):
    __tablename__ = 't_players'
    __table_args__ = (
        db.Index('idx_usergame', 'cuse', 'cgam', unique=True),
    )

    id = db.Column(db.Integer, primary_key=True)
    cgam = db.Column(db.Integer)
    cuse = db.Column(db.Integer)
    csid = db.Column(db.Integer)


class Turn(db.Model):
    __tablename__ = 't_turns'

    id = db.Column(db.Integer, primary_key=True)
    cgam = db.Column(db.Integer, db.ForeignKey('t_games.id'))
    cturn = db.Column(db.Integer)
    name = db.Column(db.String(100))

    thcoun = db.relationship('HCounter', backref='t_turns')


class User(UserMixin, db.Model):
    __tablename__ = 't_users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75))
    mail = db.Column(db.String(75))
    passwdhash = db.Column(db.String(128))

    userrol = db.relationship('RArousr', backref='t_users')
    userplay = db.relationship('Player', backref='t_users')

    def __repr__(self):
        return '<User {}>'.format(self.name)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.passwdhash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.passwdhash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
