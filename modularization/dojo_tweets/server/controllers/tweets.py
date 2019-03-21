from flask import render_template, request, redirect, session, url_for, flash
from server.models.tweets import Tweet

def create():
    errors = Tweet.validate(request.form)
    if errors:
        for error in errors:
            flash(error)
    Tweet.create(request.form, session['user_id'])
    return redirect(url_for("dashboard"))