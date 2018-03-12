#-*- coding:utf-8 -*-

from flask import Blueprint
from flask_admin import Admin
from flask_admin.contrib.sqlamodel import ModelView

from views import *
from ..models import *
from .. import db

blueprint_admin = Blueprint('crm_admin', __name__)

admin = Admin()

def init_app(app):
    admin.init_app(app)
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

    app.logger.debug("load admin succeed")
