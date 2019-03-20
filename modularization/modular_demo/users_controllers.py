from flask import render_template, request, redirect, flash
from models import User

def index():
    return render_template('index.html')

def users_create():
    errors = User.validate(request.form)
    if errors:
        for error in errors:
            flash(error)
        return redirect('/')
    User.create(request.form)
    return redirect('/success')

def success():
    return render_template('success.html')