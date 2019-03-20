from flask import render_template, request, redirect, session, url_for, flash
from sqlalchemy.sql import func
import re
from config import app, db, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

# MODELS
# TODO: Modularize into separate files
likes_table=db.Table('likes',
    db.Column(
        'tweet_id',
        db.Integer,db.ForeignKey(
            'tweets.id',
            ondelete="cascade"
        ),
        primary_key=True
    ),
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),
    db.Column(
        'created_at',
        db.DateTime,
        server_default=func.now()
    )
)

followers_table = db.Table('followers',
    db.Column(
        'follower_id',
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),
    db.Column(
        'followee_id',
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),
    db.Column(
        'created_at',
        db.DateTime,
        server_default=func.now()
    )
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    pw_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime,
        server_default=func.now()
    )
    updated_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )
    users_following_self = db.relationship('User',
        secondary=followers_table,
        primaryjoin=id==followers_table.c.followee_id,
        secondaryjoin=id==followers_table.c.follower_id,
        backref="users_self_followed",
        cascade="all"
    )

    def __repr__(self):
        return "<User: %s>" % self.username

    def __str__(self):
        return "<User: %s>" % self.username

    @classmethod
    def validate(cls, form):
        errors = []
        if len(form['first_name']) < 2:
            errors.append("First name must be at least 2 characters long.")
        if len(form['last_name']) < 2:
            errors.append("Last name must be at least 2 characters long.")
        if not EMAIL_REGEX.match(form['email']):
            errors.append("Email must be valid.")

        existing_emails = cls.query.filter_by(email=form['email']).first()
        if existing_emails:
            errors.append("Email already in use.")
        
        if len(form['username']) < 5:
            errors.append("Username must be at least 5 characters long.")
        
        existing_usernames = cls.query.filter_by(username=form['username']).first()
        if existing_usernames:
            errors.append('Username already in use.')

        if len(form['password']) < 8:
            errors.append("Password must be at least 8 characters long.")

        return errors
    
    @classmethod
    def create(cls, form):
        pw_hash = bcrypt.generate_password_hash(form['password'])
        user = cls(
            first_name=form['first_name'],
            last_name=form['last_name'],
            email=form['email'],
            username=form['username'],
            pw_hash=pw_hash,
        )
        db.session.add(user)
        db.session.commit()
        # make user a follower of self by default
        user.users_self_followed.append(user)
        db.session.commit()
        return user.id
    
    @classmethod
    def login_helper(cls, form):
        user = cls.query.filter_by(email=form['email']).first()
        if user:
            if bcrypt.check_password_hash(user.pw_hash, form['password']):
                return (True, user.id)
        return (False, "Email or password incorrect.")

class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime,
        server_default=func.now()
    )
    updated_at = db.Column(
        db.DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )
    user=db.relationship(
        'User',
        foreign_keys=[user_id],
        backref=db.backref(
            "tweets",
            cascade="all, delete-orphan"
        )
    )
    liked_by=db.relationship(
        'User',
        secondary=likes_table,
        backref="liked_tweets"
    )

    @classmethod
    def validate(cls, form):
        errors = []
        if len(form['content']) > 255:
            errors.append("Tweet cannot exceed 255 characters in length.")
        if len(form['content']) < 1:
            errors.append("Tweet must not be left empty.")
        return errors

    @classmethod
    def create(cls, form, user_id):
        tweet = cls(
            content=form['content'],
            user_id=user_id
        )
        db.session.add(tweet)
        db.session.commit()

    @classmethod
    def get_tweets_from_users(cls, user_ids=None):
        if not user_ids:
            return cls.query.order_by(cls.created_at.desc()).all()
        
        return cls.query.filter(cls.user_id.in_(user_ids)).order_by(cls.created_at.desc()).all()

# CONTROLLERS
# TODO: Modularize into separate files

# Dashboard
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
# Users
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
# Tweets
def tweets_create():
    errors = Tweet.validate(request.form)
    if errors:
        for error in errors:
            flash(error)
    Tweet.create(request.form, session['user_id'])
    return redirect(url_for("dashboard"))

# ROUTES
# TODO: Modularize into separate files

# Dashboard
app.add_url_rule('/', view_func=root, endpoint="root")
app.add_url_rule('/dashboard', view_func=dashboard, endpoint="dashboard")
# Users
app.add_url_rule('/users/new', view_func=users_new, endpoint="users:new")
app.add_url_rule('/users/create', view_func=users_create, endpoint="users:create", methods=['POST'])
app.add_url_rule('/users/login', view_func=users_login, endpoint="users:login", methods=['POST'])
app.add_url_rule('/users/logout', view_func=users_logout, endpoint="users:logout")
# Tweets
app.add_url_rule('/tweets/create', view_func=tweets_create, endpoint="tweets:create", methods=['POST'])

if __name__ == "__main__":
    app.run(debug=True)