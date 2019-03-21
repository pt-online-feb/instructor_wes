from flask import render_template, request, redirect, session, url_for, flash
from server.models.users import User
from server.models.tweets import Tweet

def root():
    if 'user_id' not in session:
        return redirect(url_for('users:new'))
    return redirect(url_for('dashboard'))

def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('users:new'))

    current_user = User.query.get(session['user_id'])

    # get all tweets
    all_tweets = Tweet.get_tweets_from_users()

    # get only tweets from users_self_followed
    # user_following_ids = [u.id for u in current_user.users_self_followed]
    # followed_tweets = Tweet.get_tweets_from_users(user_ids=user_following_ids)
    return render_template(
        'dashboard.html',
        user=current_user,
        tweets=all_tweets
    )