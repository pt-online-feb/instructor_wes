from flask import render_template, request, redirect, session, url_for, flash
from server.models.users import User

def users_new():
    return render_template('users_new.html')

def users_create():
    errors = User.validate(request.form)
    if errors:
        for error in errors:
            flash(error)
        return redirect(url_for('users:new'))
    user_id = User.create(request.form)
    session['user_id'] = user_id
    return redirect(url_for("dashboard"))

def users_login():
    valid, response = User.login_helper(request.form)
    if not valid:
        flash(response)
        return redirect(url_for("users:new"))
    session['user_id'] = response
    return redirect(url_for("dashboard"))

def users_logout():
    session.clear()
    return redirect(url_for("users:new"))