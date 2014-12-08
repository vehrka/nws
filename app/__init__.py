from config import config
from flask import Flask
from flask.ext.bootstrap import Bootstrap

bootstrap = Bootstrap()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config.from_envvar('SNWSETTINGS')
    config[config_name].init_app(app)

    from .main import main_blueprint
    app.register_blueprint(main_blueprint)

    bootstrap.init_app(app)

    return app
