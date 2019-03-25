from flask import render_template, request, redirect, session, url_for, flash
from server.models.users import User
from server.models.resume_items import ResumeItem

def root():
    if 'user_id' not in session:
        return redirect(url_for('users:new'))
    return redirect(url_for('dashboard'))

def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('users:new'))

    current_user = User.query.get(session['user_id'])
    resume_items = ResumeItem.query.filter_by(user_id=session['user_id']).all()

    return render_template(
        'dashboard.html',
        user=current_user,
        resume_items=resume_items
    )