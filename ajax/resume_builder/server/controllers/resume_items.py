from flask import render_template, request, redirect, session, url_for, flash
from server.models.resume_items import ResumeItem

def create():
    errors = ResumeItem.validate(request.form)
    if errors:
        for error in errors:
            flash(error)
    else:
        ResumeItem.create(request.form, session['user_id'])
    return redirect(url_for('dashboard'))