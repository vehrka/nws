# coding: utf-8
from . import db, login_manager
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class AApprole(db.Model):
    __tablename__ = 'a_approle'

    apr_capr = db.Column(db.Integer, primary_key=True)
    apr_desc = db.Column(db.String(100))

    roluser = db.relationship('RArousr', backref='a_approle')

    def __repr__(self):
        return '<Rol {}>'.format(self.apr_desc)


class RArousr(db.Model):
    __tablename__ = 'r_arousr'

    rru_crru = db.Column(db.Integer, primary_key=True)
    rru_capr = db.Column(db.Integer, db.ForeignKey('a_approle.apr_capr'))
    rru_cuse = db.Column(db.Integer, db.ForeignKey('t_users.use_cuse'))


class TUser(UserMixin, db.Model):
    __tablename__ = 't_users'

    use_cuse = db.Column(db.Integer, primary_key=True)
    use_username = db.Column(db.String(75))
    use_usermail = db.Column(db.String(75))
    use_passwdhash = db.Column(db.String(128))

    userrol = db.relationship('RArousr', backref='t_users')

    def __repr__(self):
        return '<User {}>'.format(self.use_username)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return TUser.query.get(int(user_id))
