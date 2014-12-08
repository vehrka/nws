#!/usr/bin/env python
# −*− coding: UTF−8 −*−

from fabric.api import execute, lcd, local, prefix, task
import os

DIR = os.path.abspath(os.path.dirname(__file__))


@task
def rundev():
    """Sets the dev environment and launches the app"""
    confpth = os.path.join(DIR, 'config/dev.cfg')
    with prefix('export SNWSETTINGS={0}'.format(confpth)):
        execute(apprun)


@task
def shelldev():
    """Sets the dev environment and launches the shell"""
    confpth = os.path.join(DIR, 'config/dev.cfg')
    with prefix('export SNWSETTINGS={0}'.format(confpth)):
        execute(shellrun)


@task
def runprod():
    """Sets the production environment and launches the app"""
    confpth = os.path.join(DIR, 'config/prod.cfg')
    with prefix('export SNWSETTINGS={0}'.format(confpth)):
        execute(apprun)


def apprun():
    local('python manage.py runserver')


def shellrun():
    local('python manage.py shell')


@task
def gendb():
    """Generates the models from the diagram"""
    with lcd('dbmodels'):
        local("parsediasql uml --file dbmodels.dia --db 'sqlite3' > dbmodels_sqlite3.sql")
        local('sqlite3 dbmodels.db < dbmodels_sqlite3.sql')
        local('sqlacodegen sqlite:///dbmodels.db > models.py')
        local('rm dbmodels_sqlite3.sql dbmodels.db')
