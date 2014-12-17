from config import config
from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config.from_envvar('SNWSETTINGS')
    config[config_name].init_app(app)

    from .main import main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .admin import admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .api_1_0 import api_1_0_blueprint as api
    app.register_blueprint(api, url_prefix='/api/v1.0')

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    return app
