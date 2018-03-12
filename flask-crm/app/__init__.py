#-*- coding:utf-8 -*-

from flask import Flask, render_template, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta

from .config import configs

from datetime import datetime
'''
json串行化
'''
class AlchemyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o.__class__, DeclarativeMeta):
            data = {}
            fields = o.__json__() if hasattr(o, '__json__') else dir(o)
            for field in [f for f in fields if not f.startswith('_') and f not in ['metadata', 'query', 'query_class']]:
                value = o.__getattribute__(field)
                try:
                    if isinstance(value, datetime):
                        value = value.strftime('%Y-%m-%d %H:%M:%S')
                    json.dumps(value)
                    data[field] = value
                except TypeError:
                    data[field] = None
            return data
        return json.JSONEncoder.default(self, o)

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    configs[config_name].init_app(app)

    app.json_encoder = AlchemyEncoder

    db.init_app(app)

    # routes

    # errors

    # blueprints
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from admin import blueprint_admin
    from admin import init_app as blueprint_admin_init_app
    app.register_blueprint(blueprint_admin)
    blueprint_admin_init_app(app)

    from principal import blueprint_principal
    from principal import init_app as blueprint_principal_init_app
    app.register_blueprint(blueprint_principal)
    blueprint_principal_init_app(app)

    app.logger.debug("load all blueprint succeed")

    return app
