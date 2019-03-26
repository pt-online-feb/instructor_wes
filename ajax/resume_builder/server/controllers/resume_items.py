from flask import render_template, request, redirect, session, url_for, flash
from server.models.resume_items import ResumeItem

def create():
    print(request.form)
    errors = ResumeItem.validate(request.form)
    if errors:
        for error in errors:
            flash(error)
        return render_template('/partials/errors.html'), 500
    else:
        ResumeItem.create(request.form, session['user_id'])
    # return redirect(url_for('dashboard'))
    return "SUCCESS"

def current_user(user_id):
    resume_items = ResumeItem.query.filter_by(user_id=user_id).all()
    return render_template('partials/resume_items.html', items=resume_items)