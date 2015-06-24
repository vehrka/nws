#!/usr/bin/env python
# −*− coding: UTF−8 −*−

from fabric.api import lcd, local, prefix, task
import os

DIR = os.path.abspath(os.path.dirname(__file__))


@task
def test():
    """Runs the unittests"""
    local('python manage.py test')


@task
def rundev():
    """Sets the dev environment and launches the app"""
    exportcfg = os.path.join(DIR, 'EXPORTME.cfg')
    with prefix('export APP_CONFIG={}'.format(exportcfg)):
        apprun()


@task
def shelldev():
    """Sets the dev environment and launches the shell"""
    exportcfg = os.path.join(DIR, 'EXPORTME.cfg')
    with prefix('export APP_CONFIG={}'.format(exportcfg)):
        shellrun(confpth)


@task
def dbcmm(cmmd):
    """Sets the dev environment and gives the command to Migrate"""
    exportcfg = os.path.join(DIR, 'EXPORTME.cfg')
    with prefix('export APP_CONFIG={}'.format(exportcfg)):
        dbrun(cmmd)


@task
def initdb():
    """Sets the dev environment and launches the shell"""
    exportcfg = os.path.join(DIR, 'EXPORTME.cfg')
    with prefix('export APP_CONFIG={}'.format(exportcfg)):
        dbinit()


def apprun():
    local('python manage.py runserver')


def shellrun():
    local('python manage.py shell')


def dbrun(cmnd):
    local('python manage.py db {}'.format(cmnd))


def dbinit():
    local('python manage.py db init')
    local('python manage.py db migrate')
    local('python manage.py db upgrade')
    local('python manage.py seed')


@task
def genmoddb():
    """Generates the models from the diagram"""
    with lcd('dbmodels'):
        local("parsediasql uml --file dbmodels.dia --db 'sqlite3' > dbmodels_sqlite3.sql")
        local('sqlite3 dbmodels.db < dbmodels_sqlite3.sql')
        local('sqlacodegen sqlite:///dbmodels.db > models.py')
        local('sed -i -f sedcmd.txt models.py')
        local('rm dbmodels_sqlite3.sql dbmodels.db')
