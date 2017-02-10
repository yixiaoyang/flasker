from datetime import datetime
from flask import render_template, session, redirect, url_for, escape, request, flash, abort
from ..models import *
from . import main
from .. import db
from run import app

from flask_login import login_required,login_user

#from ..models import User
#from .froms import NameForm

@main.route('/',methods=['get', 'post'])
def index():
    return render_template('index.html')

#####################################################################
# Todo
#####################################################################
@main.route('/todo/',methods=['get', 'post'])
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
            flash('You were successfully inssert new todo',"success")
    todos = Todo.query.all()
    todos_count = Todo.query.count()
    return render_template('todo/index.html', todos=todos,todos_count=todos_count)

# test:curl -i http://localhost:5000/todo/1/ -X DELETE
@main.route('/todo/<id>/',methods=['get','post', 'delete'])
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
    print('method = %s' % request)
    if request.method == 'GET':
       return '<h1>hello, iam goiing to login[GET]</h1>'
    else:
        return '<h1>hello, iam goiing to login[POST]</h1>'

#####################################################################
# Company
#####################################################################
@main.route('/company/', methods=['get','post'])
def companies():
    error = None
    if request.method == 'POST':
        company = Company()
        company.name = request.form['name'] or ''
        company.address = request.form['address'] or ''
        company.business = request.form['business'] or ''
        db.session.add(company)
        db.session.commit()
        flash('You were successfully inssert new company',"success")
        return redirect(url_for('main.companies'))
    companies = Company.query.all()
    companies_count = Company.query.count()
    return render_template('company/index.html', companies=companies, companies_count=companies_count)

@main.route('/company/remove/<id>',methods=['get','post','delete'])
def company_remove(id):
    company = Company.query.filter_by(id=id).first()
    if company is None:
        abort(404)
    db.session.delete(company)
    db.session.commit()
    return redirect(url_for('main.companies'))

@main.route('/company/show/<id>',methods=['get'])
def company_show(id):
    company = Company.query.filter_by(id=id).first()
    if company is None:
        abort(404)
    return render_template('company/show.html', company=company)


#####################################################################
# Customer
#####################################################################
@main.route('/customer/', methods=['get','post'])
def customers():
    error = None
    customers = Customer.query.all()
    customers_count = Customer.query.count()
    return render_template('customer/index.html', customers=customers, customers_count=customers_count)

@main.route('/customer/remove/<id>',methods=['get','post','delete'])
def customer_remove(id):
    customer = Customer.query.filter_by(id=id).first()
    if customer is None:
        abort(404)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('main.customers'))

@main.route('/customer/show/<id>',methods=['get'])
def customer_show(id):
    customer = Customer.query.filter_by(id=id).first()
    if customer is None:
        abort(404)
    return render_template('customer/show.html', customer=customer)

@main.route('/customer/new/',methods=['get','post'])
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
        flash('You were successfully inssert new customer',"success")
        return redirect(url_for('main.customer_show',id=customer.id))
    elif  request.method == 'GET':
        app.logger.info("customer_new get done")
        companies = Company.query.all()
        return render_template('customer/new_form.html', companies=companies)


@main.route('/customer/update/<id>',methods=['get','post'])
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
        flash('You were successfully inssert new customer',"success")
        return redirect(url_for('main.customer_show',id=customer.id))
    elif  request.method == 'GET':
        customer = Customer.query.filter_by(id=id).first()
        companies = Company.query.all()
        return render_template('customer/update_form.html', companies=companies, customer=customer)


#####################################################################
# Product
#####################################################################
@main.route('/product/', methods=['get','post'])
def products():
    error = None
    if request.method == 'POST':
        product = Product()
        product.name = request.form['name'] or ''
        product.description = request.form['description'] or ''
        db.session.add(product)
        db.session.commit()
        flash('You were successfully inssert new product',"success")
        return redirect(url_for('main.products'))
    products = Product.query.all()
    products_count = Product.query.count()
    return render_template('product/index.html', products=products, products_count=products_count)

@main.route('/product/remove/<id>',methods=['get','post','delete'])
def product_remove(id):
    product = Product.query.filter_by(id=id).first()
    if product is None:
        abort(404)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('main.products'))

@main.route('/product/show/<id>',methods=['get'])
def product_show(id):
    product = Product.query.filter_by(id=id).first()
    if product is None:
        abort(404)
    return render_template('product/show.html', product=product)
