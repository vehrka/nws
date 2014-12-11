from flask import render_template, session, redirect, url_for
from . import main_blueprint


@main_blueprint.route('/')
def index():
    return render_template('index.html')
