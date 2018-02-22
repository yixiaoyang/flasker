#-*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateTimeField
from wtforms import IntegerField, DateField, SelectField

from wtforms.validators import DataRequired, EqualTo, Email, Length

class LoginForm(FlaskForm):
    title = ''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',  validators=[DataRequired()])

class RegisterForm(FlaskForm):
    title = ''
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Password must match')
    ])
    confirm = PasswordField('Repeat Password')
    email = StringField('Email Address', [Email(), Length(min=6, max=64)])

class NewMachineForm(FlaskForm):
    title = '新建设备资料'
    # 唯一id
    serial =  StringField(label='设备编号', validators=[DataRequired(), Length(max=32)])
    hw_version = StringField(label='主板版本号')
    regulate_done = BooleanField(label='是否完成校准', default=False)
    regulate_on = DateTimeField(label='完成校准日期', format='%Y-%m-%d %H:%M:%S')
    product_id = SelectField(label='产品类型', coerce=int)
    license_type = IntegerField(label="License类型", default=0)
