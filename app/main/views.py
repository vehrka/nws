from flask import render_template, session, redirect, url_for
from flask.ext.login import login_required
from app.decorators import admin_required
from . import main_blueprint


@main_blueprint.route('/')
def index():
    return render_template('index.html')


@main_blueprint.route('/admin')
@login_required
@admin_required
def admin():
    parent = 'admin'
    return render_template('admin.html', parent=parent)
