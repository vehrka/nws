#!/usr/bin/env python
# −*− coding: UTF−8 −*−

from fabric.api import execute, local, prefix, task
import os

DIR = os.path.abspath(os.path.dirname(__file__))


@task
def test():
    confpth = os.path.join(DIR, 'config/test.cfg')
    with prefix('export SNWSETTINGS={0}'.format(confpth)):
        execute(apprun)


@task
def prod():
    confpth = os.path.join(DIR, 'config/prod.cfg')
    with prefix('export SNWSETTINGS={0}'.format(confpth)):
        execute(apprun)


def apprun():
    local('python manage.py runserver')
