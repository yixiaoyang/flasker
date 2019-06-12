#-*- coding:utf-8 -*-

import os
import sys

from flask import url_for
from flask_script import Manager,Shell
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_scss import Scss
from flask_ckeditor import CKEditor
from logging.handlers import RotatingFileHandler
from celery import Celery

import logging
from app import create_app, db

def make_celery(app):
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
celery = make_celery(app)

# logging
log_handler = RotatingFileHandler('run.log', maxBytes=10240, backupCount=1)
log_handler.setLevel(logging.DEBUG)
app.logger.addHandler(log_handler)

# initialization for componet
manager = Manager(app)
migreate = Migrate(app,db)
#ckeditor = CKEditor(app)
Scss(app)

def make_shell_context():
	return dict(app=app, db=db)

manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

# python run.py list_routes
@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:32s} {:32s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print (line)

if __name__ == '__main__':
	manager.run()
