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
        return '<Rol {}>'.format(self.apr_desc)


class RArousr(db.Model):
    __tablename__ = 'r_arousr'

    id = db.Column(db.Integer, primary_key=True)
    capr = db.Column(db.Integer, db.ForeignKey('a_approle.id'))
    cuse = db.Column(db.Integer, db.ForeignKey('t_users.id'))


class User(UserMixin, db.Model):
    __tablename__ = 't_users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75))
    mail = db.Column(db.String(75))
    passwdhash = db.Column(db.String(128))

    userrol = db.relationship('RArousr', backref='t_users')

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
