# coding: utf-8
from . import db, login_manager
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Side(db.Model):
    __tablename__ = 'a_sides'

    id = db.Column(db.Integer, primary_key=True)
    acro = db.Column(db.String(15))
    desc = db.Column(db.String(75))

    sideplay = db.relationship('Player', backref='a_sides')

    @staticmethod
    def insert_sides():
        sides = {'USN': (1, 'United States Navy'),
                 'KM': (2, 'Kriegsmarine'),
                 'RN': (3, 'Royal Navy'),
                 'FFNF': (4, 'Free France Naval Forces'),
                 'RM': (5, 'Regia Marina'),
                 'IJN': (6, 'Imperial Japanese Navy'),
                 'SN': (7, 'Soviet Navy'),
                 'RAN': (8, 'Royal Australian Navy'),
                 'SAN': (9, 'Armada Nacional'),
                 'SAR': (10, 'Armada Republicana')}
        for s in sides:
            side = Side.query.filter_by(acro=s).first()
            if side is None:
                side = Side(acro=s)
                side.id = sides[s][0]
            side.desc = sides[s][1]
            db.session.add(side)
        db.session.commit()

    def __repr__(self):
        return '<Side {}>'.format(self.desc)


class RArousr(db.Model):
    __tablename__ = 'r_arousr'

    id = db.Column(db.Integer, primary_key=True)
    capr = db.Column(db.Integer, db.ForeignKey('a_approle.id'))
    cuse = db.Column(db.Integer, db.ForeignKey('t_users.id'))


class ShpClass(db.Model):
    __tablename__ = 'a_shpclasses'

    id = db.Column(db.Integer, primary_key=True)
    acro = db.Column(db.String(15))
    desc = db.Column(db.String(100))

    clacoun = db.relationship('Counter', backref='a_shpclasses')
    clahcoun = db.relationship('HCounter', backref='a_shpclasses')

    @staticmethod
    def insert_classes():
        classes = {'CV': (1, 'Aircraft Carrier'),
                   'CVE': (2, 'Escort Aircraft Carrier'),
                   'CVL': (3, 'Light Aircraft Carrier'),
                   'BB': (4, 'Battleship'),
                   'BC': (5, 'Battle Cruiser'),
                   'CA': (6, 'Heavy Cruiser'),
                   'CL': (7, 'Light Cruiser'),
                   'DD': (8, 'Destroyer'),
                   'DE': (9, 'Destroyer Escort'),
                   'DL': (10, 'Destroyer Leader'),
                   'SS': (11, 'Submarine'),
                   'SSC': (12, 'Coastal Submarine'),
                   'AE': (13, 'Ammunition Ship'),
                   'AF': (14, 'Store Ship'),
                   'AFS': (15, 'Combat Store Ship'),
                   'AO': (16, 'Oiler'),
                   'APD': (17, 'Destroyer Transport'),
                   'DMS': (18, 'Destroyer Minesweeper'),
                   'MSO': (19, 'Minesweeper'),
                   'ML': (20, 'Minelayer'),
                   'PG': (21, 'Gunboat'),
                   'PB': (22, 'Patrol Boat'),
                   'PT': (23, 'Patrol Torpedo')}
        for c in classes:
            aclass = ShpClass.query.filter_by(acro=c).first()
            if aclass is None:
                aclass = ShpClass(acro=c)
                aclass.id = classes[c][0]
            aclass.desc = classes[c][1]
            db.session.add(aclass)
        db.session.commit()

    def __repr__(self):
        return '<Counter Class {}>'.format(self.desc)


class Counter(db.Model):
    __tablename__ = 't_counters'

    id = db.Column(db.Integer, primary_key=True)
    cclas = db.Column(db.Integer, db.ForeignKey('a_shpclasses.id'))
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
    cclas = db.Column(db.Integer, db.ForeignKey('a_shpclasses.id'))
    ccou = db.Column(db.Integer, db.ForeignKey('t_counters.id'))
    name = db.Column(db.String(100))
    bearing = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    height = db.Column(db.Integer)
    detected = db.Column(db.Boolean)
    cturn = db.Column(db.Integer, db.ForeignKey('t_turns.id'))
    lat = db.Column(db.Integer)
    lon = db.Column(db.Integer)


class Turn(db.Model):
    __tablename__ = 't_turns'

    id = db.Column(db.Integer, primary_key=True)
    cgam = db.Column(db.Integer, db.ForeignKey('t_games.id'))
    cturn = db.Column(db.Integer)
    name = db.Column(db.String(100))

    thcoun = db.relationship('HCounter', backref='t_turns')


class Player(db.Model):
    __tablename__ = 't_players'
    __table_args__ = (
        db.Index('idx_usergame', 'cuse', 'cgam', unique=True),
    )

    id = db.Column(db.Integer, primary_key=True)
    cgam = db.Column(db.Integer, db.ForeignKey('t_games.id'))
    cuse = db.Column(db.Integer, db.ForeignKey('t_users.id'))
    csid = db.Column(db.Integer, db.ForeignKey('a_sides.id'))


class Approle(db.Model):
    __tablename__ = 'a_approle'

    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.String(100))

    #roluser = db.relationship('RArousr', backref=db.backref('a_approle', lazy='dynamic'), lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {'admin': (1,),
                 'user': (10,)}
        for r in roles:
            role = Approle.query.filter_by(desc=r).first()
            if role is None:
                role = Approle(desc=r)
                role.id = roles[r][0]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Rol {}>'.format(self.desc)


class User(UserMixin, db.Model):
    __tablename__ = 't_users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75))
    mail = db.Column(db.String(75))
    passwdhash = db.Column(db.String(128))

    userrol = db.relationship('RArousr', foreign_keys=[RArousr.cuse], backref=db.backref('t_users', lazy='joined'), lazy='dynamic')
    userplay = db.relationship('Player', foreign_keys=[Player.cuse], backref=db.backref('t_users', lazy='joined'), lazy='dynamic')

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

    def is_admin(self):
        aid = Approle.query.filter_by(desc='admin').first().id
        if self.userrol.filter_by(capr=aid).first():
            return True
        else:
            return False


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
