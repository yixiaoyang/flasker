#-*- coding:utf-8 -*-

from flask import render_template, session, redirect, url_for, escape, request
from flask import flash, abort
from flask import Flask, Response
from flask.ext.principal import Permission, RoleNeed

from . import blueprint_principal

# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))

# protect a view with a principal for that need
@blueprint_principal.route('/admin')
@admin_permission.require()
def admin_index():
    print("get in blueprint_principal /admin")
    return Response('Only if you are an admin')
