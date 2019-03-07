from flask import Flask, redirect, session, render_template, request, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

SCHEMA = "app_generator"

app = Flask(__name__)
app.secret_key = "asdf;alkjsdf;lakjsdfas;dlkjf"
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/users/new')
    
    query = "SELECT email FROM users WHERE id=%(user_id)s;"
    data = {
        "user_id": session['user_id']
    }
    db = connectToMySQL(SCHEMA)
    users = db.query_db(query, data)
    user = users[0]

    query = "SELECT * FROM app_names;"
    db = connectToMySQL(SCHEMA)
    app_names = db.query_db(query)

    return render_template('index.html',
                            email=user['email'],
                            app_names=app_names
                            )

@app.route('/users/new')
def users_new():
    return render_template('users_new.html')

@app.route('/users/create', methods=['POST'])
def users_create():
    errors = []

    query = "SELECT id FROM users WHERE email=%(email)s;"
    data = {
        'email': request.form['email']
    }
    db = connectToMySQL(SCHEMA)
    existing_users = db.query_db(query, data)

    if len(existing_users) > 0:
        errors.append("A user exists with that email")

    if not EMAIL_REGEX.match(request.form['email']):
        errors.append("Email must be valid")
    
    if len(request.form['password']) < 8:
        errors.append("Password must be at least 8 characters")

    if len(errors) > 0:
        for error in errors:
            flash(error)
        return redirect('/users/new')

    # hash password
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    query = "INSERT INTO users (email, password) VALUES(%(email)s, %(password)s);"
    data = {
        "email": request.form['email'],
        "password": pw_hash
    }
    db = connectToMySQL(SCHEMA)
    user_id = db.query_db(query, data)
    session['user_id'] = user_id
    return redirect('/')

@app.route('/users/login', methods=['POST'])
def login():
    # SELECT email
    query = "SELECT id, password FROM users WHERE email=%(email)s;"
    data = {
        'email': request.form['email']
    }
    db = connectToMySQL(SCHEMA)
    existing_users = db.query_db(query, data)
    if len(existing_users) > 0:
        user = existing_users[0]
        if bcrypt.check_password_hash(user['password'], request.form['password']):
            session['user_id'] = user['id']
            return redirect('/')

    flash("Email or password incorrect")
    return redirect('/users/new')

@app.route('/app_names/create', methods=['POST'])
def app_names_create():
    errors = []
    if len(request.form['name']) < 1:
        errors.append("Must not be left blank")
    
    query = "SELECT * FROM app_names WHERE name=%(name)s;"
    data = {
        "name": request.form['name']
    }
    db = connectToMySQL(SCHEMA)
    existing_app_names = db.query_db(query, data)
    if existing_app_names:
        errors.append("Name already used")
    
    if errors:
        for error in errors:
            flash(error)
    else:
        query = "INSERT INTO app_names (name, user_id) VALUES (%(name)s, %(user_id)s);"
        data = {
            'user_id': session['user_id'],
            'name': request.form['name']
        }
        db = connectToMySQL(SCHEMA)
        db.query_db(query, data)
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/users/new')

if __name__ == "__main__":
    app.run(debug=True)