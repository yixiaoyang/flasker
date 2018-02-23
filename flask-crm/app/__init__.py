#-*- coding:utf-8 -*-

from flask import Flask, render_template, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask_login import LoginManager
from config import config

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
                    json.dumps(value)
                    data[field] = value
                except TypeError:
                    data[field] = None
            return data
        return json.JSONEncoder.default(self, o)

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = "main.login"
login_manager.login_message = u'请先登陆CRM系统'
login_manager.login_message_category = "error"

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.json_encoder = AlchemyEncoder

    db.init_app(app)
    login_manager.init_app(app)

    # routes

    # errors

    # blueprint
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    print("register blueprint succeed")
    return app
