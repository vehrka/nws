#!/usr/bin/env python
# −*− coding: UTF−8 −*−

from fabric.api import lcd, local, prefix, task
import os

DIR = os.path.abspath(os.path.dirname(__file__))


@task
def rundev():
    """Sets the dev environment and launches the app"""
    confpth = os.path.join(DIR, 'config/dev.cfg')
    with prefix('export FLASK_CONFIG=development'):
        apprun(confpth)


@task
def shelldev():
    """Sets the dev environment and launches the shell"""
    confpth = os.path.join(DIR, 'config/dev.cfg')
    with prefix('export FLASK_CONFIG=development'):
        shellrun(confpth)


@task
def dbcmm(cmmd):
    """Sets the dev environment and gives the command to Migrate"""
    confpth = os.path.join(DIR, 'config/dev.cfg')
    with prefix('export FLASK_CONFIG=development'):
        dbrun(confpth, cmmd)


@task
def runprod():
    """Sets the production environment and launches the app"""
    confpth = os.path.join(DIR, 'config/prod.cfg')
    with prefix('export FLASK_CONFIG=production'):
        apprun(confpth)


def apprun(confpth):
    with prefix('export SNWSETTINGS={0}'.format(confpth)):
        local('python manage.py runserver')


def shellrun(confpth):
    with prefix('export SNWSETTINGS={0}'.format(confpth)):
        local('python manage.py shell')


def dbrun(confpth, cmnd):
    with prefix('export SNWSETTINGS={0}'.format(confpth)):
        local('python manage.py db {}'.format(cmnd))


@task
def gendb():
    """Generates the models from the diagram"""
    with lcd('dbmodels'):
        local("parsediasql uml --file dbmodels.dia --db 'sqlite3' > dbmodels_sqlite3.sql")
        local('sqlite3 dbmodels.db < dbmodels_sqlite3.sql')
        local('sqlacodegen sqlite:///dbmodels.db > models.py')
        local('rm dbmodels_sqlite3.sql dbmodels.db')
