from flask import render_template, request, redirect, session, url_for, flash
from server.models.users import User

def new():
    return render_template('users_new.html')

def create():
    errors = User.validate(request.form)
    if errors:
        for error in errors:
            flash(error)
        return redirect(url_for('users:new'))
    user_id = User.create(request.form)
    session['user_id'] = user_id
    return redirect(url_for("dashboard"))

def login():
    valid, response = User.login_helper(request.form)
    if not valid:
        flash(response)
        return redirect(url_for("users:new"))
    session['user_id'] = response
    return redirect(url_for("dashboard"))

def logout():
    session.clear()
    return redirect(url_for("users:new"))

def first_name():
    user = User.query.get(session['user_id'])
    return user.first_name