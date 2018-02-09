#-*- coding:utf-8 -*-

from app import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager

from datetime import datetime

'''
UserMixin:  使用Flask-Login继承UserMixin，实现相关接口
'''
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),unique=True, index=True)
    username = db.Column(db.String(64),unique=True, index=True)
    password_hash = db.Column(db.String(128))
    authenticated = db.Column(db.Boolean, default=False)
    registered_on = db.Column('registered_on' , db.DateTime)

    # 建立user和issue_record之间的外键关系
    my_issue_records = db.relationship('IssueRecord', backref='author')

    def __init__(self, name, passwd, mail=''):
        self.username = name
        self.password_hash = generate_password_hash(passwd)
        self.email = mail
        self.authenticated = False
        self.registered_on = datetime.utcnow()

    def __repr__(self):
        return '<User %r>' % (self.username)

    @property
    def password(self):
        raise AttributeError('Password is not readable attriute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)

    # Flask-Login interface is_authenticated, is_active, get_id, is_anonymous
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def is_anonymous(self):
        return False

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
    def __repr__(self):
        return '<Todo %r>' % self.id

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    address = db.Column(db.String(128))
    business = db.Column(db.Text())

    # Company有多个Customer（联系人）
    employees = db.relationship('Customer', backref='my_company')
    def __repr__(self):
        return '<Company %r %r>' % (self.id, self.name)

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    # Customer（联系人） 属于一个公司, customer.company
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
    def __repr__(self):
        return '<Customer %r>' % self.name

'''
装配日期
主板序号
CPU序号
软件版本
软件期限
AC版本
DC版本
出厂日期
客户公司
鼠键序号
TF卡容量
'''
class ProductConfig(db.Model):
    __tablename__ = 'product_config'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text())

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
    note = db.Column(db.Text())

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
