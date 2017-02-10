#-*- coding:utf-8 -*-

from app import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager

from datetime import datetime

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),unique=True, index=True)
    username = db.Column(db.String(64),unique=True, index=True)
    password_hash = db.Column(db.String(128))

    # 建立user和issue_record之间的外键关系
    my_issue_records = db.relationship('IssueRecord', backref='author')

    @property
    def password(self):
        raise AttributeError('Password is not readable attriute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Todo(db.Model):
    content = db.Column(db.String(64))
    time = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.Integer,default=0)
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, content, status):
        self.content = content
        self.status = status

    # 返回一个可读性的字符串表示模型，可在调试和测试时使用
    def _repr_(self):
        return '<Todo %r>' % self.id

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    address = db.Column(db.String(128))
    business = db.Column(db.Text())

    # 建立一个‘my_company’的反向引用供Customer查询自己的公司
    employees = db.relationship('Customer', backref='my_company')
    def _repr_(self):
        return '<Todo %r>' % self.name

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    name = db.Column(db.String(128))
    address = db.Column(db.String(128))
    email = db.Column(db.String(64))
    qq = db.Column(db.String(16))
    tel = db.Column(db.String(32))
    mobile = db.Column(db.String(32))
    position = db.Column(db.String(64))
    note = db.Column(db.String(1024))
    buy_records = db.relationship('SellRecord', backref='customer')

    def _repr_(self):
        return '<Todo %r>' % self.name

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text())
    sell_records = db.relationship('SellRecord', backref='product')

class Issue(db.Model):
    __tablename__ = 'issues'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.Text())
    type = db.Column(db.Integer)
    status = db.Column(db.Integer)

class IssueRecord(db.Model):
    __tablename__ = 'issue_records'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.Text())
    create_time = db.Column(db.DateTime,default=datetime.now())
    readonly = db.Column(db.Boolean(),default=False)

class SellRecord(db.Model):
    __tablename__ = 'sell_records'
    id = db.Column(db.Integer, primary_key=True)
    product_id  = db.Column(db.Integer,db.ForeignKey('products.id') ,  index=True)
    customer_id = db.Column(db.Integer,db.ForeignKey('customers.id'),  index=True)
    price = db.Column(db.Float, default=0.0)
    # 每个销售出去的机器有一个唯一编号
    serial = db.Column(db.String(64))
    date = db.Column(db.DateTime,default=datetime.now())

class ServiceRecord(db.Model):
    __tablename__ = 'service_records'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, index=True)
    customer_id = db.Column(db.Integer, index=True)
    date = db.Column(db.DateTime,default=datetime.now())

class VisitRecord(db.Model):
    __tablename__ = 'visit_records'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, index=True)
    date = db.Column(db.DateTime,default=datetime.now())
