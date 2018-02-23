#-*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms.validators import Optional
from wtforms import StringField, PasswordField, BooleanField, DateTimeField
from wtforms import IntegerField, DateField, SelectField, TextAreaField

from wtforms.validators import DataRequired, EqualTo, Email, Length
from ..models import Product, Machine

class LoginForm(FlaskForm):
    title = ''
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码',  validators=[DataRequired()])

class RegisterForm(FlaskForm):
    title = ''
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[
        DataRequired(),
        EqualTo('confirm', message='密码必须一致')
    ])
    confirm = PasswordField('重复密码')
    email = StringField('Email地址', [Email(), Length(min=6, max=64)])

class NewMachineForm(FlaskForm):
    title = '新建设备资料'
    # 唯一id
    serial =  StringField(label='设备编号', validators=[DataRequired(), Length(max=32)])
    hw_version = StringField(label='主板版本号')
    regulate_done = BooleanField(label='是否完成校准', default=False)
    regulate_on = DateTimeField(label='完成校准日期', format='%Y-%m-%d %H:%M:%S',
        validators=[Optional()])
    product_id = SelectField(label='产品类型', coerce=int)
    license_type = SelectField(label="License类型", default=0, coerce=int,
        choices= [(i, Machine.licenseStr(i)) for i in range(3)])

class NewProductForm(FlaskForm):
    title = '新建产品类型'
    name =  StringField(label='产品名', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField(label='描述')
    status = SelectField(label="研发状态", default=0, coerce=int,
        choices= [(i,Product.statusStr(i)) for i in range(4)])
