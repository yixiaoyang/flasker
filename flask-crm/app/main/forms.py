#-*- coding:utf-8 -*-

from flask_wtf import FlaskForm
from wtforms.validators import Optional
from wtforms import StringField, PasswordField, BooleanField, DateTimeField
from wtforms import IntegerField, DateField, SelectField, TextAreaField, HiddenField
from flask_ckeditor import CKEditorField

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
    old_id =  HiddenField(label='old_id', validators=[Optional()])
    id =  StringField(label='设备编号', validators=[DataRequired(), Length(max=32)])
    status = SelectField(label="状态", default=0, coerce=int,
        choices= [(i, Machine.statusStr(i)) for i in range(7)])
    hw_version = StringField(label='主板版本号')
    ac_version = StringField(label='FPGA AC版本号')
    dc_version = StringField(label='FPGA DC版本号')
    description = TextAreaField(label='备注')
    manufactured_on = DateTimeField(label='出厂日期', format='%Y-%m-%d %H:%M:%S',
        validators=[Optional()])
    regulate_done = BooleanField(label='是否完成校准', default=False)
    regulate_on = DateTimeField(label='完成校准日期', format='%Y-%m-%d %H:%M:%S',
        validators=[Optional()])
    product_id = SelectField(label='产品类型', coerce=int)
    license = SelectField(label="License类型", default=0, coerce=int,
        choices= [(i, Machine.licenseStr(i)) for i in range(3)])
    license_to = DateTimeField(label='License日期', format='%Y-%m-%d %H:%M:%S',
        validators=[Optional()])
    company_id = SelectField(label="所在公司", default=0, coerce=int,
        choices= [], validators=[Optional()])

    tf_capacity = IntegerField(label="TF卡容量(G)", default=8, validators=[Optional()])
    mouse_keyboard = BooleanField(label="配备鼠标键盘", default=8)

    check_ac_volt = BooleanField(label="检查AC电压",  default=False)
    check_normal_test = BooleanField(label="检查常规测试",default=False)
    check_cv = BooleanField(label="检查CV模式",  default=False)
    check_cr = BooleanField(label="检查CR模式",  default=False)
    check_hv = BooleanField(label="检查高压测试",default=False)

    def copy_to(self, machine):
        machine.product_id = self.product_id.data
        machine.company_id = self.company_id.data
        machine.status = self.status.data
        machine.hw_version = self.hw_version.data
        machine.ac_version = self.ac_version.data
        machine.dc_version = self.dc_version.data
        machine.description = self.description.data
        machine.regulate_done = self.regulate_done.data
        machine.regulate_on = self.regulate_on.data
        machine.manufactured_on = self.manufactured_on.data
        machine.license = self.license.data
        machine.license_to = self.license_to.data
        machine.tf_capacity = self.tf_capacity.data
        machine.mouse_keyboard = self.mouse_keyboard.data
        machine.check_ac_volt = self.check_ac_volt.data
        machine.check_normal_test = self.check_normal_test.data
        machine.check_cv = self.check_cv.data
        machine.check_hv = self.check_hv.data
        machine.check_cr = self.check_cr.data

class NewProductForm(FlaskForm):
    title = '新建产品类型'
    id = HiddenField(label='id')
    name =  StringField(label='产品名', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField(label='描述')
    status = SelectField(label="研发状态", default=0, coerce=int,
        choices= [(i,Product.statusStr(i)) for i in range(4)])


class NewCompanyForm(FlaskForm):
    title = '新建客户公司资料'
    id = HiddenField(label='id')
    name =  StringField(label='公司名', validators=[DataRequired(), Length(max=128)])
    address = StringField(label='地址', validators=[Optional()])
    business = TextAreaField(label='描述', validators=[Optional()])
