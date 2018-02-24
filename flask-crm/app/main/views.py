#-*- coding:utf-8 -*-

import logging
from datetime import datetime
from flask import render_template, session, redirect, url_for, escape, request
from flask import flash, abort, jsonify, json
from ..models import *
from . import main
from .. import db
from run import app

# forms
from .forms  import LoginForm, RegisterForm, NewMachineForm, NewProductForm

from flask_login import login_required, login_user, logout_user, current_user
from flask_login import login_required

@main.route('/',methods=['get', 'post'])
@login_required
def index():
    return render_template('index.html')

#####################################################################
# Todo
#####################################################################
@main.route('/todo/',methods=['get', 'post'])
@login_required
def todos():
    error = None
    if request.method == 'POST':
        content = request.form['content']
        if not content:
            error = "Invalid Content"
        else:
            todo = Todo(content=content,status=0)
            db.session.add(todo)
            db.session.commit()
            print todo
            flash('You were successfully inssert new todo','success')
    todos = Todo.query.all()
    todos_count = Todo.query.count()
    return render_template('todo/index.html', todos=todos,todos_count=todos_count)

# test:curl -i http://localhost:5000/todo/1/ -X DELETE
@main.route('/todo/<id>/',methods=['get','post', 'delete'])
@login_required
def todos_show(id):
    print('method = %s' % request)
    if request.method == 'GET':
        todo = Todo.query.filter_by(id=id).first()
        if todo is None:
            abort(404)
        return render_template('todo/show.html', todo=todo)
    elif request.method == 'DELETE':
        # url_for in blueprint 'url_for(BlueprintName.FuncName)'
        return redirect(url_for('main.todos'))

@main.route('/todo/del/<id>',methods=['get','post','delete'])
@login_required
def todos_del(id):
    #id = request.form['id']
    print('id=%s' % id)
    todo = Todo.query.filter_by(id=id).first()
    if todo is None:
        abort(404)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('main.todos'))


#####################################################################
# User
#####################################################################
@main.route('/user/login/', methods=['post','get'])
def login():
    '''
    [GET]:  display the login form
    [POST]: login the current user by processing the form
    '''
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm(request.form)
    form.title = '登录系统'
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        #user = User(form.username.data, form.password.data)
        if user:
            if user.verify_password(form.password.data):
                login_user(user)
                flash('登录成功','success')
                print("User %s %s login user succeed" % (user.username,current_user.username))
                return redirect(url_for('main.index'))
            else:
                flash('用户名或者密码错误','error')
                return render_template("user/login.html", form=form)
    return render_template("user/login.html",  form=form)

@main.route('/user/logout/')
@login_required
def logout():
    logout_user()
    flash('您已注销登录')
    form = LoginForm(request.form)
    form.title = '登录系统'
    return render_template("user/login.html",  form=form)

@main.route('/user/register/', methods=['post','get'])
def register():
    form = RegisterForm(request.form)
    form.title = '注册'
    if form.validate_on_submit():
        user = User(form.username.data, form.password.data, form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功，请在邮箱中查找确认链接进行验证')
        return render_template('index.html')
    return render_template("user/register.html",  form=form)


#####################################################################
# Company
#####################################################################
@main.route('/company/', methods=['get','post'])
@login_required
def companies():
    error = None
    if request.method == 'POST':
        company = Company()
        company.name = request.form['name'] or ''
        company.address = request.form['address'] or ''
        company.business = request.form['business'] or ''
        db.session.add(company)
        db.session.commit()
        flash('创建成功','success')
        return redirect(url_for('main.companies'))
    companies = Company.query.all()
    companies_count = Company.query.count()
    return render_template('company/index.html', companies=companies, companies_count=companies_count)

@main.route('/company/remove/<id>',methods=['get','post','delete'])
@login_required
def company_remove(id):
    company = Company.query.filter_by(id=id).first()
    if company is None:
        abort(404)
    db.session.delete(company)
    db.session.commit()
    return redirect(url_for('main.companies'))

@main.route('/company/show/<id>',methods=['get'])
@login_required
def company_show(id):
    company = Company.query.filter_by(id=id).first()
    if company is None:
        abort(404)
    print(company)
    print("name:%s"%company.name)
    return render_template('company/show.html', company=company)


#####################################################################
# Customer
#####################################################################
@main.route('/customer/', methods=['get','post'])
@login_required
def customers():
    error = None
    customers = Customer.query.all()
    companies = Company.query.all()
    customers_count = len(customers)
    logging.debug("all companies count:%d"%len(companies))
    return render_template('customer/index.html', customers=customers, companies=companies, customers_count=customers_count)

@main.route('/customer/remove/<id>',methods=['get','post','delete'])
@login_required
def customer_remove(id):
    customer = Customer.query.filter_by(id=id).first()
    if customer is None:
        abort(404)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('main.customers'))

@main.route('/customer/show/<id>',methods=['get'])
@login_required
def customer_show(id):
    customer = Customer.query.filter_by(id=id).first()
    if customer is None:
        abort(404)
    return render_template('customer/show.html', customer=customer)

@main.route('/customer/new/',methods=['get','post'])
@login_required
def customer_new():
    error = None
    if request.method == 'POST':
        customer = Customer()
        company_id = request.form['company'] or ''
        if company_id:
            company = Company.query.filter_by(id=company_id).first()
            if company:
                customer.company_id = company.id
            else:
                print("error: can't find company_id %s" % company_id)
        customer.name = request.form['name'] or ''
        customer.address = request.form['address'] or ''
        customer.email = request.form['email'] or ''
        customer.qq = request.form['qq'] or ''
        customer.tel = request.form['tel'] or ''
        customer.mobile = request.form['mobile'] or ''
        customer.position = request.form['position'] or ''
        customer.note = request.form['note'] or ''

        db.session.add(customer)
        db.session.commit()
        flash('创建成功','success')
        return redirect(url_for('main.customers'))
        #return redirect(url_for('main.customer_show',id=customer.id))
    elif  request.method == 'GET':
        app.logger.info("customer_new get done")
        companies = Company.query.all()
        logging.debug("all companies count:%d"%len(companies))
        return render_template('customer/new_form.html', companies=companies)


@main.route('/customer/update/<id>',methods=['get','post'])
@login_required
def customer_update(id):
    error = None
    customer = None
    if request.method == 'POST':
        if id:
            customer = Customer.query.filter_by(id=id).first()
        if not customer:
            abort(404)
        customer.name = request.form['name'] or ''
        customer.address = request.form['address'] or ''
        customer.email = request.form['email'] or ''
        customer.qq = request.form['qq'] or ''
        customer.tel = request.form['tel'] or ''
        customer.mobile = request.form['mobile'] or ''
        customer.position = request.form['position'] or ''
        customer.note = request.form['note'] or ''
        customer.company_id = request.form['company'] or '0'

        db.session.add(customer)
        db.session.commit()
        flash('创建成功','success')
        return redirect(url_for('main.customer_show',id=customer.id))
    elif  request.method == 'GET':
        customer = Customer.query.filter_by(id=id).first()
        companies = Company.query.all()
        return render_template('customer/update_form.html', companies=companies, customer=customer)


#####################################################################
# Product
#####################################################################
@main.route('/product/', methods=['get','post'])
@login_required
def products():
    error = None

    form = NewProductForm(request.form)
    if request.method == 'POST':
        product = Product()
        product.name = form.name.data
        product.description = form.description.data
        product.status = form.status.data
        db.session.add(product)
        db.session.commit()
        flash('创建成功','success')
        return redirect(url_for('main.products'))
    products = Product.query.all()
    products_count = len(products)
    return render_template('product/index.html', products=products, products_count=products_count, form=form)

@main.route('/product/remove/<id>',methods=['get','post','delete'])
@login_required
def product_remove(id):
    product = Product.query.filter_by(id=id).first()
    if product is None:
        abort(404)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('main.products'))

@main.route('/product/show/<id>',methods=['get'])
@login_required
def product_show(id):
    product = Product.query.filter_by(id=id).first()
    if product is None:
        abort(404)
    return render_template('product/show.html', product=product)

@main.route('/product/edit/',methods=['post'])
@login_required
def product_edit():
    print("get in product_edit")
    params = request.get_json()
    if params:
        id = params['id']
        form = NewProductForm(request.form)
        product = Product.query.filter_by(id=id).first()
        if product is None:
            abort(404)
        print(product)
        print(json.dumps(product))
        form.description.data = product.description
        form.status.data = product.status
        form.name.data = product.name
        return json.dumps(product)
    else:
        abort(404)

@main.route('/product/update/',methods=['post'])
@login_required
def product_update():
    params = request.form
    if params:
        form = NewProductForm(params)
        product = Product.query.filter_by(id=form.id.data).first()
        if product:
            product.status = form.status.data
            product.name = form.name.data
            product.description = form.description.data
            db.session.commit()
            print("update done")
    return redirect(url_for('main.products'))

#####################################################################
# SellRecord
#####################################################################
@main.route('/sell_record/', methods=['get','post'])
@login_required
def sell_records():
    records = SellRecord.query.all()
    records_count = SellRecord.query.count()
    return render_template('sell_record/index.html', records=records, sell_records_count=records_count)

@main.route('/sell_record/remove/<id>',methods=['get','post','delete'])
@login_required
def sell_record_remove(id):
    record = SellRecord.query.filter_by(id=id).first()
    if record is None:
        abort(404)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('main.sell_records'))

@main.route('/sell_record/show/<id>',methods=['get'])
@login_required
def sell_record_show(id):
    record = SellRecord.query.filter_by(id=id).first()
    if record is None:
        abort(404)
    return render_template('sell_record/show.html', record=record)

@main.route('/sell_record/new/',methods=['get','post'])
@login_required
def sell_record_new():
    error = None
    app.logger.info("request.method=%s"%request.method)
    if request.method == 'POST':
        sell_record = SellRecord()
        customer_id = request.form['customer'] or ''
        product_id = request.form['product'] or ''
        app.logger.info("customer.id, product.id=%s/%s"%(customer_id, product_id))
        if customer_id:
            customer = Customer.query.filter_by(id=customer_id).first()
            if customer:
                sell_record.customer_id = customer.id
            else:
                abort(500)
        if product_id:
            product = Product.query.filter_by(id=product_id).first()
            if product:
                sell_record.product_id = product.id
            else:
                abort(500)

        sell_record.price = float(request.form['price']) or 0.0
        sell_record.serial = request.form['serial'] or ''
        sell_record.note = request.form['note'] or ''
        sell_record.date = datetime.strptime(request.form['date'] or '', "%Y-%m-%d %H:%M:%S")
        db.session.add(sell_record)
        db.session.commit()
        flash('成功新建销售记录','success')
        return redirect(url_for('main.sell_record_show',id=sell_record.id))
    elif  request.method == 'GET':
        customers = Customer.query.all()
        products = Product.query.all()
        return render_template('sell_record/new_form.html', products=products, customers=customers)

#####################################################################
# Machines
#####################################################################
@main.route('/machine/', methods=['get','post'])
@login_required
def machines():
    error = None

    form = NewMachineForm(request.form)
    products = Product.query.all()
    form.product_id.choices = [(p.id, p.name) for p in products]

    companies = Company.query.all()
    form.company_id.choices = [(p.id, p.name) for p in companies]

    if request.method == 'POST':
        if form.validate():
            machine = Machine(id=form.id.data)

            form.copy_to(machine)
            #machine.product_id = form.product_id.data
            #machine.status = form.status.data
            #machine.hw_version = form.hw_version.data
            #machine.regulate_done = form.regulate_done.data
            #machine.regulate_on = form.regulate_on.data
            #machine.license = form.license.data
            #machine.tf_capacity = form.tf_capacity.data
            #machine.mouse_keyboard = form.mouse_keyboard.data
            #machine.check_ac_volt = form.check_ac_volt.data
            #machine.check_normal_test = form.check_normal_test.data
            #machine.check_cv = form.check_cv.data
            #machine.check_hv = form.check_hv.data
            #machine.check_cr = form.check_cr.data

            db.session.add(machine)
            db.session.commit()
            flash('创建成功','success')
            return redirect(url_for('main.machines'))
        else:
            print("machine create error:")
            for err in form.errors:
                print(err, form.product_id.data)

    machines = Machine.query.all()
    machines_count = len(machines)
    return render_template('machine/index.html', machines=machines,
                            machines_count=machines_count, form=form)

@main.route('/machine/remove/<id>',methods=['get','post','delete'])
@login_required
def machine_remove(id):
    machine = Machine.query.filter_by(id=id).first()
    if machine is None:
        abort(404)
    db.session.delete(machine)
    db.session.commit()
    return redirect(url_for('main.machines'))

@main.route('/machine/show/<id>',methods=['get'])
@login_required
def machine_show(id):
    machine = Machine.query.filter_by(id=id).first()
    if machine is None:
        abort(404)
    return render_template('machine/show.html', machine=machine)


@main.route('/machine/edit/',methods=['post'])
@login_required
def machine_edit():
    params = request.get_json()
    if params:
        print(params)

        id = params['id']
        form = NewMachineForm(request.form)
        machine = Machine.query.filter_by(id=id).first()
        if machine is None:
            abort(404)

        #print(machine.__json__())
        #for name in machine.__json__():
        #    value = getattr(machine,name)
        #    print(name,value)

        return json.dumps(machine)
    else:
        abort(404)

@main.route('/machine/update/',methods=['post'])
@login_required
def machine_update():
    params = request.form
    if params:
        print(params)
        form = NewMachineForm(params)

        old_id = form.old_id.data
        new_id = form.id.data

        if old_id and (old_id != new_id):
            machine = Machine.query.filter_by(id=old_id).first()
            if not machine:
                abort(404)
            machine.id = new_id
        else:
            machine = Machine.query.filter_by(id=form.id.data).first()
            if not machine:
                abort(404)

        form.copy_to(machine)

        #machine.product_id = form.product_id.data
        #machine.status = form.status.data
        #machine.hw_version = form.hw_version.data
        #machine.regulate_done = form.regulate_done.data
        #machine.regulate_on = form.regulate_on.data
        #machine.license = form.license.data
        #machine.tf_capacity = form.tf_capacity.data
        #machine.mouse_keyboard = form.mouse_keyboard.data
        #machine.check_ac_volt = form.check_ac_volt.data
        #machine.check_normal_test = form.check_normal_test.data
        #machine.check_cv = form.check_cv.data
        #machine.check_hv = form.check_hv.data
        #machine.check_cr = form.check_cr.data

        db.session.commit()
        print("update done")
    return redirect(url_for('main.machines'))
