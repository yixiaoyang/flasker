#-*- coding:utf-8 -*-

import os
import sys

from flask import url_for
from flask_script import Manager,Shell
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_scss import Scss
from flask_admin import Admin
from flask_admin.contrib.sqlamodel import ModelView

import logging
from logging.handlers import RotatingFileHandler

from flask_ckeditor import CKEditor

from app import create_app, db
from app.models import *

reload(sys)
sys.setdefaultencoding('utf-8')

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# admin
admin = Admin(app)
admin.add_view(ModelView(User, db.session, category="系统"))
admin.add_view(ModelView(Company, db.session, category="客户"))
admin.add_view(ModelView(Customer, db.session, category="客户"))
admin.add_view(ModelView(ProductConfig, db.session, category="产品"))
admin.add_view(ModelView(Product, db.session, category="产品"))
admin.add_view(ModelView(Machine, db.session, category="产品"))
admin.add_view(ModelView(Issue, db.session, category="跟踪"))
admin.add_view(ModelView(IssueRecord, db.session, category="跟踪"))
admin.add_view(ModelView(SellRecord, db.session, category="跟踪"))
admin.add_view(ModelView(ServiceRecord, db.session, category="跟踪"))
admin.add_view(ModelView(VisitRecord, db.session, category="跟踪"))
admin.add_view(ModelView(Todo, db.session, category="跟踪"))



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
        print line

if __name__ == '__main__':
	manager.run()
