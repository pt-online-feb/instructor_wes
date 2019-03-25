from sqlalchemy.sql import func
from config import db, bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
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

    def __repr__(self):
        return "<User: %s>" % self.email

    def __str__(self):
        return "<User: %s>" % self.email

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
            pw_hash=pw_hash,
        )
        db.session.add(user)
        db.session.commit()
        return user.id
    
    @classmethod
    def login_helper(cls, form):
        user = cls.query.filter_by(email=form['email']).first()
        if user:
            if bcrypt.check_password_hash(user.pw_hash, form['password']):
                return (True, user.id)
        return (False, "Email or password incorrect.")