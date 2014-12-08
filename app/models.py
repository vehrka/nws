# coding: utf-8
from . import db


class AApprole(db.Model):
    __tablename__ = 'a_approle'

    apr_capr = db.Column(db.Integer, primary_key=True)
    apr_desc = db.Column(db.String(100))

    roluser = db.relationship('RArousr', bacref='a_approle')

    def __repr__(self):
        return '<Rol {}>'.format(self.apr_desc)


class RArousr(db.Model):
    __tablename__ = 'r_arousr'

    rru_crru = db.Column(db.Integer, primary_key=True)
    rru_capr = db.Column(db.Integer, db.ForeignKey('a_approle.apr_capr'))
    rru_cuse = db.Column(db.Integer, db.ForeignKey('t_users.use_cuse'))


class TUser(db.Model):
    __tablename__ = 't_users'

    use_cuse = db.Column(db.Integer, primary_key=True)
    use_username = db.Column(db.String(75))
    use_passwdhash = db.Column(db.String(128))

    userrol = db.relationship('RArousr', bacref='t_users')

    def __repr__(self):
        return '<User {}>'.format(self.use_username)
