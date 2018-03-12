#-*- coding:utf-8 -*-

from flask import Blueprint
from flask_login import LoginManager
from flask.ext.principal import Principal

blueprint_principal = Blueprint('crm_principal', __name__)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = "main.login"
login_manager.login_message = u'请先登陆CRM系统'
login_manager.login_message_category = "error"

# load the extension
principals = Principal()

def init_app(app):
    # login
    login_manager.init_app(app)

    # load the extension
    principals.init_app(app)

    app.logger.debug("load login_manager and principals succeed")

from views import *
