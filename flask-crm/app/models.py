#-*- coding:utf-8 -*-

from . import db
from principal import login_manager

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

'''
权限表
'''
class Permission:
    # 基本权限
    READ = 0x1
    APPEND = 0x2
    DELETE = 0x4
    MODIFY = 0x8

    # 1024
    ALL = 0x400

    # 操作对象
    User = 0x1
    Company = 0x2
    Customer = 0x3
    Product = 0x4
    Machine = 0x5
    Issue = 0x6
    IssueRecord = 0x7
    SellRecord = 0x8
    ServiceRecord = 0x9
    VisitRecord = 0xA

    @staticmethod
    def get(table, operation):
        return 2048 * operation+table
class PermissionTable:
    def __init__(self):
        ptable = {
            User.__tablename__: Permission.READ,
            Company.__tablename__: Permission.READ+Permission.APPEND,
            Customer.__tablename__: Permission.READ+Permission.APPEND,
            Product.__tablename__: Permission.READ+Permission.APPEND,
            Machine.__tablename__: Permission.READ+Permission.APPEND,
            Issue.__tablename__: Permission.READ+Permission.APPEND,
            IssueRecord.__tablename__: Permission.READ+Permission.APPEND,
            SellRecord.__tablename__: Permission.READ+Permission.APPEND,
            ServiceRecord.__tablename__: Permission.READ+Permission.APPEND,
            VisitRecord.__tablename__: Permission.READ+Permission.APPEND
        }

    def toStr():

        pass

    def fromStr(strs):
        pass

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

'''
公司信息类
'''
class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    address = db.Column(db.String(128))
    business = db.Column(db.Text())

    # Company有多个Customer（联系人）
    employees = db.relationship('Customer', backref='my_company')

    # 客户公司拥有的机器
    machines = db.relationship('Machine', backref='company')

    def __repr__(self):
        return '<Company %r %r>' % (self.id, self.name)

    @staticmethod
    def __json__():
        return ['id', 'name', 'address', 'business']

'''
客户信息类
'''
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

class ProductConfig(db.Model):
    __tablename__ = 'product_config'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text())


'''
产品信息类
'''
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    status = db.Column(db.Integer())
    description = db.Column(db.Text())
    sell_records = db.relationship('SellRecord', backref='product')
    machines = db.relationship('Machine', backref='product')

    @staticmethod
    def statusStr(val):
        if val is None:
            return ""
        choices=['未规划','规划中','研发中','完成研发']
        if val > len(choices):
            return ""
        return choices[val]

    @staticmethod
    def __json__():
        return ['id', 'name', 'status', 'description']

'''
机器记录
一个销售纪录可能包含多台机器
一个机器只有一个产品型号
'''
class Machine(db.Model):
    __tablename__ = 'machines'

    # 机器序号
    id = db.Column(db.String(32), primary_key=True)

    '''
    关联外键
    '''
    # 外键到产品型号
    product_id  = db.Column(db.Integer, db.ForeignKey('products.id'), default=0)

    # 外键到销售记录条目
    sell_record_id = db.Column(db.Integer, db.ForeignKey('sell_records.id'), index=True, default=0)

    # 外键到出货公司
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))

    issues = db.relationship('Issue', backref='machine')

    '''
    基本信息
    '''
    # 设备状态
    # 0：空闲
    # 1：校准中
    # 2：试用中
    # 3：已出货（半款）
    # 4：已出货（全款）
    # 5：返修中
    # 6：已回收
    status = db.Column(db.Integer, default=0)
    description = db.Column(db.Text())

    '''
    机器配置
    '''
    # 主板版本
    hw_version = db.Column(db.String(64))
    # 软件版本
    soft_version = db.Column(db.String(64))
    # AC/DC FPGA版本
    ac_version = db.Column(db.String(64))
    dc_version = db.Column(db.String(64))
    # 组装出厂时间
    manufactured_on = db.Column('manufactured_on' , db.DateTime)
    # license类型， 0:试用版，1:企业版，2：内部样机
    license = db.Column(db.Integer, default=0)
    # 软件版本期限
    license_to = db.Column('license_to' , db.DateTime)
    # TF Card容量，单位G
    tf_capacity = db.Column(db.Integer, default=8)
    # 鼠标键盘
    mouse_keyboard = db.Column(db.Boolean(), default=True)

    '''
    校准和检查记录
    '''
    # 检查AC电压
    check_ac_volt = db.Column(db.Boolean(), default=False)
    # 常规测试
    check_normal_test = db.Column(db.Boolean(), default=False)
    # 检查CV模式
    check_cv = db.Column(db.Boolean(), default=False)
    # 检查CR模式
    check_cr = db.Column(db.Boolean(), default=False)
    # 检查高压测试
    check_hv = db.Column(db.Boolean(), default=False)
    # 校准完毕
    regulate_done = db.Column(db.Boolean(), default=False)
    # 校准日期
    regulate_on = db.Column('regulate_on' , db.DateTime)

    def __init__(self, id=''):
        self.id = id

    @staticmethod
    def __json__():
        return ['id', 'company_id', 'status', 'hw_version', 'manufactured_on',
        'regulate_done', 'regulate_on', 'product_id', 'license',
        'tf_capacity', 'mouse_keyboard', 'check_ac_volt', 'check_normal_test',
        'check_cv', 'check_cr', 'check_hv', 'license_to', 'description',
        'dc_version','ac_version']

    @staticmethod
    def licenseStr(val):
        if val is None:
            return ""
        choices=['试用版','企业版','内部样机']
        if val >= len(choices):
            return ""
        return choices[val]

    @staticmethod
    def statusStr(val):
        if val is None:
            return ""
        strs = [
            # 0:
            "空闲",
            # 1：
            "校准中",
            # 2：
            "试用中",
            # 3：
            "已半款",
            # 4：
            "已结清",
            # 5：
            "返修中",
            # 6：
            "已回收"
        ]
        if val > len(strs):
            return ""
        return strs[val]

'''
issue和machine是一对一关系
'''
Product_Issue_Relationship_Table = db.Table('product_issue',
    db.Model.metadata,
    db.Column('product_id', db.Integer, db.ForeignKey('products.id')),
    db.Column('issue_id', db.Integer, db.ForeignKey('issues.id'))
)

class Issue(db.Model):
    __tablename__ = 'issues'
    id = db.Column(db.Integer, primary_key=True)

    # 关联到出问题的机器
    machine_id = db.Column(db.String(32), db.ForeignKey('machines.id'))

    # 关联到一系列产品
    products = db.relationship('Product', secondary=Product_Issue_Relationship_Table,
                               backref= 'issues')

    title = db.Column(db.String(128))
    description = db.Column(db.Text())
    # 0：需求，1：反馈，2：功能问题，3：性能问题，4：其他
    type = db.Column(db.Integer)
    # 0：新建/opened
    # 1：正在解决/working
    # 2：正在测试/待反馈/testing
    # 3：已解决/fixed
    # 4：延后解决/pending
    # 5：忽略/ignored
    status = db.Column(db.Integer)

class IssueRecord(db.Model):
    __tablename__ = 'issue_records'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description = db.Column(db.Text())
    create_time = db.Column(db.DateTime,default=datetime.now())
    readonly = db.Column(db.Boolean(),default=False)

'''
一条销售记录包含多台机器
'''
class SellRecord(db.Model):
    __tablename__ = 'sell_records'
    id = db.Column(db.Integer, primary_key=True)
    product_id  = db.Column(db.Integer, db.ForeignKey('products.id') ,  index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'),  index=True)
    price = db.Column(db.Float, default=0.0)
    # 每个销售出去的机器有一个唯一编号
    serial = db.Column(db.String(64))
    date = db.Column(db.DateTime,default=datetime.now())
    note = db.Column(db.Text())

    machines = db.relationship('Machine', backref='sell_record')

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
