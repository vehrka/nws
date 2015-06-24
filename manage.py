#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Approle, RArousr, Side, ShpClass, Game, Player
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from datetime import datetime

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Approle=Approle, RArousr=RArousr)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    """For data seeding the Database"""
    print('Seeding Sides')
    Side.insert_sides()
    print('Seeding Ship Clases')
    ShpClass.insert_classes()
    print('Seeding Roles')
    Approle.insert_roles()
    print('Seeding Users')
    u1 = User(id=1, name='vehrka', mail='vehrka@gmail.com')
    u1.password = 'cat'
    db.session.add(u1)
    u2 = User(id=2, name='edsombra', mail='edsombra@edsombra.es')
    u2.password = 'dog'
    db.session.add(u2)
    db.session.commit()
    print('Seeding User Roles')
    ra1 = RArousr(id=1, capr=1, cuse=1)
    ra2 = RArousr(id=2, capr=10, cuse=1)
    ra3 = RArousr(id=3, capr=10, cuse=2)
    db.session.add(ra1)
    db.session.add(ra2)
    db.session.add(ra3)
    db.session.commit()
    print('Seeding Games')
    g1 = Game(id=1, name='test1', desc='test game', date=datetime(2014, 12, 20, 18, 52, 48), finished=0)
    db.session.add(g1)
    g2 = Game(id=2, name='test2', desc='test finished stuff', date=datetime(2014, 12, 22, 9, 28, 56), finished=1)
    db.session.add(g1)
    db.session.add(g2)
    db.session.commit()
    print('Seeding Games Players')
    p1 = Player(id=1, cgam=1, cuse=1, csid=1)
    p2 = Player(id=2, cgam=1, cuse=2, csid=6)
    p3 = Player(id=3, cgam=2, cuse=1, csid=9)
    p4 = Player(id=4, cgam=2, cuse=2, csid=10)
    db.session.add(p1)
    db.session.add(p2)
    db.session.add(p3)
    db.session.add(p4)


@manager.command
def test():
    """Run the unit test"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
